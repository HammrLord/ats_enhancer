from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import re


class ATSEnhancer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.gai = GoogleGenerativeAI(api_key=self.api_key, model="gemini-2.5-flash", temperature=0.3)
        self.rephrase_template = PromptTemplate(
            input_variables=["job_description", "resume_lines"],
            template=(
                '''
                You are an expert resume optimization assistant trained in HR, NLP, and ATS systems.
                Your task is to rewrite resume bullet points to make them more effective and ATS-friendly while \n
                preserving the original meaning and achievements.
                The rewritten lines must:
                1. Use strong action verbs at the start.
                2. Incorporate keywords from the provided job description and ATS keyword list wherever relevant.
                3. Be concise, professional, and results-oriented (avoid filler or vague phrases).
                4. Highlight quantifiable impact (add metrics or results if implied but missing).
                5. Maintain a confident but realistic tone — avoid exaggeration.
                6. Avoid using pronouns ("I", "my") or full sentences. Write in resume bullet style.
                7. Use phrases like "Attained", "Advised", "Devised", "Directed", "Enhanced", "Expanded", "Generated", "Implemented", "Led", "Optimized", "Spearheaded", etc.
                Only return all of the rewritten bullet points, starting with "•".
                **Job Description**:
                {job_description}
                **Resume Bullet Points to Enhance**:
                {resume_lines}
                '''
            )
        )
        self.evaluation_prompt = PromptTemplate(
            input_variables=["line","job_description"],
            template=(
                '''
                You are supposed to mimic the behavior of an ATS system but only for single bullet points taking the job description into account.
                First, provide a step-by-step reasoning for your score. Analyze the bullet point against these 5 criteria:
                1. Relevance to job description keywords.
                2. Use of strong action verbs.
                3. Clarity and conciseness.
                4. Presence of quantifiable achievements.
                5. Deduct points for vague language or lack of impact.
                After your reasoning, provide the final score between 0 and 100 on a new line in the format: "FINAL SCORE:[score]
                Example: [Reasoning...][newline]FINAL SCORE:85"
                **Resume Bullet Point**:
                {line}
                **Job Description**:
                {job_description}
                '''
            )
        )
        self.evaluate = self.evaluation_prompt | self.gai | StrOutputParser()
        self.paraphrase_chain = self.rephrase_template | self.gai | StrOutputParser()
    def enhance_resume(self, job_description: str, resume_lines: str):
        #batch processing can be added here if needed
        response = self.paraphrase_chain.invoke({
            "job_description": job_description,
            "resume_lines": resume_lines
        })
        return response
    def evaluate_lines(self, lines: list[str], job_description: str):
        inputs = [{"line": line, "job_description": job_description} for line in lines]
        score_strings = self.evaluate.batch(inputs)
        scores = []
        pattern = re.compile(r"FINAL SCORE\s*:\s*(\d+)", re.IGNORECASE)
        for score_raw in score_strings:
            try:
                match = pattern.search(score_raw)
                if match:
                    score = int(match.group(1).strip())
                    scores.append(score)
                else:
                    print(f"Warning: 'FINAL SCORE' not found in response. Defaulting to 0.")
                    scores.append(0)
            except (ValueError, TypeError):
                print(f"Warning: Could not parse score '{score_raw}'. Defaulting to 0.")
                scores.append(0)
        return scores
