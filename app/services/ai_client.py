from typing import Optional, Any, Dict
import json
import httpx
from app.core.config import get_settings
import re

settings = get_settings()


class AIAnalysisError(Exception):
   pass


async def analyze_resume(resume_text: str, job_description: Optional[str]) -> Dict[str, Any]:
   if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_API_KEY:
      raise AIAnalysisError("Azure OpenAI configuration is missing.")

   system_prompt = (
      "You are an expert resume reviewer. "
      "You carefully evaluate resumes and provide structured, concise feedback. "
      "Always respond in valid JSON only. No extra commentary."
   )

   jd_section = f"\n\nTarget Job Description:\n{job_description}" if job_description else ""

   user_prompt = f"""
   Resume:
   {resume_text}
   {jd_section}

   Analyse this resume and respond ONLY in valid JSON with this structure:

   {{
   "overall_score": number (0-100),
   "experience_summary": "string",
   "skills": {{
      "technical": ["skill1", "skill2"],
      "soft": ["skill1", "skill2"]
   }},
   "strengths": ["point1", "point2"],
   "gaps": ["point1", "point2"],
   "improvement_suggestions": ["point1", "point2"]
   }}
   """

   url = (
      f"{settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/"
      f"{settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions"
      f"?api-version={settings.AZURE_OPENAI_API_VERSION}"
   )

   headers = {
      "Content-Type": "application/json",
      "api-key": settings.AZURE_OPENAI_API_KEY,
   }

   payload = {
      "messages": [
         {"role": "system", "content": system_prompt},
         {"role": "user", "content": user_prompt},
      ],
      "temperature": 0.2,
   }

   async with httpx.AsyncClient(timeout=30.0) as client:
      resp = await client.post(url, json=payload, headers=headers)

   if resp.status_code != 200:
      raise AIAnalysisError(
         f"Azure OpenAI returned {resp.status_code}: {resp.text}"
      )

   data = resp.json()
   ai_response = data["choices"][0]["message"]["content"]
   pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
   match = re.search(pattern, ai_response)
   
   if match:
      json_string = match.group(1).strip()
   
   try:
      parsed = json.loads(json_string)
   except json.JSONDecodeError as e:
      raise AIAnalysisError(f"Model did not return valid JSON: {e}") from e

   return parsed
