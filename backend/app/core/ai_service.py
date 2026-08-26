import json
import httpx
from typing import Dict, Any, Optional
from app.config import settings

class AIService:
    @staticmethod
    async def get_assistive_guidance(prompt: str, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        
        # 1. Check if OpenAI API key is available
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-"):
            try:
                system_prompt = (
                    "You are JANSAHAY AI, a public-service assistant for Indian citizens. "
                    "You provide helpful, concise guidance on government certificates (Income, Domicile, Caste), "
                    "EPFO claim transfers, and citizen grievances. "
                    "You NEVER make legal decisions or change case statuses. "
                    "Return ONLY valid JSON matching this schema: "
                    '{"recommended_service_id": "INCOME_CERTIFICATE"|"DOMICILE_CERTIFICATE"|"EPFO_CLAIM_TRANSFER"|"STREET_LIGHT_GRIEVANCE"|null, '
                    '"service_title": string, "explanation": string, "confidence_score": float}'
                )
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            "response_format": {"type": "json_object"},
                            "temperature": 0.2
                        }
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data["choices"][0]["message"]["content"]
                        return json.loads(content)
            except Exception:
                pass # Fallback to deterministic matcher below

        # Deterministic Intelligent Matcher (Offline / Demo Safe)
        if any(w in prompt_lower for w in ["income", "aamdani", "scholarship", "fee concession", "earning", "2 lakh", "lakhs", "salary"]):
            return {
                "recommended_service_id": "INCOME_CERTIFICATE",
                "service_title": "Income Certificate",
                "explanation": "Based on your query regarding income verification or educational fee concessions, you should apply for an Income Certificate. You will need: 1. Identity Proof (Aadhaar/Voter ID), 2. Salary Slip or Income Declaration, and 3. Central Delhi Residence Proof.",
                "confidence_score": 0.96
            }
        elif any(w in prompt_lower for w in ["epfo", "pf", "provident fund", "uan", "pension", "company transfer"]):
            return {
                "recommended_service_id": "EPFO_CLAIM_TRANSFER",
                "service_title": "EPFO Claim / Transfer",
                "explanation": "To transfer Provident Fund accumulations from your previous employer to your current establishment, you can submit an EPFO Online Transfer Request. You will need your active UAN and previous establishment member ID.",
                "confidence_score": 0.95
            }
        elif any(w in prompt_lower for w in ["domicile", "residence", "native", "niwas", "praman patra", "stay"]):
            return {
                "recommended_service_id": "DOMICILE_CERTIFICATE",
                "service_title": "Domicile / Residence Certificate",
                "explanation": "To prove permanent residency within the state for government recruitment or admissions, apply for a Domicile Certificate. Requires 3+ years continuous address verification.",
                "confidence_score": 0.94
            }
        elif any(w in prompt_lower for w in ["light", "street", "road", "garbage", "drain", "water", "complaint", "grievance", "sewage"]):
            return {
                "recommended_service_id": "STREET_LIGHT_GRIEVANCE",
                "service_title": "Public Civic Grievance",
                "explanation": "For broken civic infrastructure such as street lights, potholes, or sanitation issues, file a Public Civic Grievance. The case is dispatched directly to the municipal zonal engineer.",
                "confidence_score": 0.97
            }
        else:
            return {
                "recommended_service_id": "INCOME_CERTIFICATE",
                "service_title": "Public Service Guidance",
                "explanation": "JANSAHAY helps you apply for statutory certificates (Income, Domicile), EPFO claims, and civic grievances. Please select a service or describe your situation.",
                "confidence_score": 0.85
            }
