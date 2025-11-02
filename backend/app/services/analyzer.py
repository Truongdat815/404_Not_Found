import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def analyze_text(text: str, model: str = "gemini-1.5-pro") -> dict:
    """
    Phân tích SRS/User Stories bằng Gemini API
    
    Args:
        text: Nội dung SRS/User Stories cần phân tích
        model: Tên model Gemini (mặc định: gemini-1.5-pro)
    
    Returns:
        dict: Kết quả phân tích với các key: conflicts, ambiguities, suggestions
    """
    try:
        # Tạo prompt cho Gemini
        prompt = f"""You are an AI assistant specialized in software requirements analysis.

Your task is to analyze the following Software Requirements Specification (SRS) or User Stories text and identify:
1. CONFLICTS: Requirements that contradict or negate each other
2. AMBIGUITIES: Requirements that are vague, unclear, or have multiple interpretations
3. SUGGESTIONS: Improved versions of requirements that are clearer and more specific

Return your analysis in valid JSON format with this exact structure:
{{
  "conflicts": [
    {{
      "req1": "requirement 1 text",
      "req2": "requirement 2 text",
      "description": "explanation of the conflict"
    }}
  ],
  "ambiguities": [
    {{
      "req": "the ambiguous requirement text",
      "issue": "explanation of why it's ambiguous"
    }}
  ],
  "suggestions": [
    {{
      "req": "original requirement text",
      "new_version": "improved, clearer version"
    }}
  ]
}}

If there are no conflicts, ambiguities, or suggestions, return empty arrays.

Text to analyze:
{text}

JSON Response:"""

        # Gọi Gemini API
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        
        # Lấy text response
        response_text = response.text.strip()
        
        # Tìm JSON trong response (có thể có markdown code block)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Parse JSON
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Nếu không parse được JSON, thử tìm JSON object trong text
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback: trả về structure rỗng với raw response
                return {
                    "conflicts": [],
                    "ambiguities": [],
                    "suggestions": [],
                    "raw_response": response_text,
                    "error": "Could not parse JSON from response"
                }
        
        # Đảm bảo structure đúng
        result.setdefault("conflicts", [])
        result.setdefault("ambiguities", [])
        result.setdefault("suggestions", [])
        
        return result
        
    except Exception as e:
        # Xử lý lỗi
        return {
            "conflicts": [],
            "ambiguities": [],
            "suggestions": [],
            "error": str(e)
        }

