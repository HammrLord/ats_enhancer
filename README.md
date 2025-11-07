# ats_enhancer
**[Link](https://atsnhancer.streamlit.app/)** 

---
##  How It Works

This tool uses the Google Gemini generative AI model (via LangChain) to act as an expert resume assistant.

1.  **Enhancement:** The app sends your current resume points and the full job description to the AI. It instructs the AI to rewrite each bullet point to be more impactful, using strong action verbs, quantifiable metrics, and keywords from the job description.
2.  **Evaluation:** The app then asks the AI to act as an ATS and score both your *original* points and the *newly enhanced* points on a scale of 0-100. The score is based on relevance, impact, and keyword alignment with the job description.
3.  **Comparison:** Finally, it displays the original and enhanced versions side-by-side with their respective scores, allowing you to see the improvement.
---
##  Inputs

* **Job Description:** The full text of the job description you are targeting. (Optional)
* **Resume:** The existing bullet points from your resume.
---
##  Future Scope

* The evaluation right now is elementary, and a much advanced version using **IRT(Item Response Theory)** can be implemented to give a more holistic score.
* The paraphrasing is done using a single call, but it can be implemented in a feedback loop manner. Where, after each try, the agent gets the updates ATS score with reasons from which it can improve the score further.
---

