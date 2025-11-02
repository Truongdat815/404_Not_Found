"""
Core agent module for analyzing SRS/User Stories
Multi-function agent with intent routing and chat interface support
Uses HTTP API to connect to FastAPI backend
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
BACKEND_AVAILABLE = True  # Always assume backend is available via HTTP

# Check if backend is reachable
try:
    response = requests.get(f"{API_BASE_URL}/health", timeout=2)
    BACKEND_AVAILABLE = response.status_code == 200
except:
    BACKEND_AVAILABLE = False
    print(f"Warning: Backend API at {API_BASE_URL} not reachable. Some features may not work.")


class Agent:
    """Agent class for analyzing requirements documents with multiple functions"""
    
    def __init__(self):
        """Initialize the agent"""
        self.api_base_url = API_BASE_URL
        self.backend_available = BACKEND_AVAILABLE
        self.current_document = None
        self.conversation_context = []
        self.current_analysis_id = None  # Store analysis ID for export
    
    def invoke(self, text: str) -> Dict[str, Any]:
        """
        Analyze SRS/User Stories text and return results (legacy method)
        
        Args:
            text: Input text to analyze (SRS/User Stories)
            
        Returns:
            Dictionary containing:
            - conflicts: List of detected conflicts
            - ambiguities: List of detected ambiguities
            - suggestions: List of improvement suggestions
            - metrics: Dictionary with analysis metrics
        """
        result = self.process_message(text, self.current_document)
        
        # Format for backward compatibility
        if "error" not in result:
            conflicts_list = [
                f"Conflict: {c.get('req1', '')} vs {c.get('req2', '')} - {c.get('description', '')}"
                for c in result.get("conflicts", [])
            ]
            ambiguities_list = [
                f"Ambiguity: {a.get('req', '')} - {a.get('issue', '')}"
                for a in result.get("ambiguities", [])
            ]
            suggestions_list = [
                f"Suggestion: {s.get('req', '')} -> {s.get('new_version', '')}"
                for s in result.get("suggestions", [])
            ]
            
            return {
                "conflicts": conflicts_list,
                "ambiguities": ambiguities_list,
                "suggestions": suggestions_list,
                "metrics": {
                    "total_conflicts": len(conflicts_list),
                    "total_ambiguities": len(ambiguities_list),
                    "total_suggestions": len(suggestions_list),
                    "text_length": len(text),
                    "requirements_count": text.count("REQ") if "REQ" in text.upper() else 1
                }
            }
        else:
            # Return mock data if there's an error
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "metrics": {
                    "total_conflicts": 0,
                    "total_ambiguities": 0,
                    "total_suggestions": 0,
                    "text_length": len(text),
                    "requirements_count": 0
                }
            }
    
    def process_message(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a chat message and route to appropriate function
        
        Args:
            text: Message text from user
            context: Optional context from previous conversation
            
        Returns:
            Dictionary with response and metadata
        """
        # Detect intent and route to appropriate function
        intent = self._detect_intent(text)
        
        if intent == "analyze_requirements":
            return self._analyze_requirements(text)
        elif intent == "answer_question":
            return self._answer_question(text, context)
        elif intent == "generate_test_cases":
            return self._generate_test_cases(text, context)
        elif intent == "explain_conflicts":
            return self._explain_conflicts(text, context)
        else:
            return self._handle_generic_message(text)
    
    def _detect_intent(self, text: str) -> str:
        """
        Detect user intent from message text
        
        Args:
            text: User message
            
        Returns:
            Intent string: analyze_requirements, answer_question, generate_test_cases, explain_conflicts, or generic
        """
        text_lower = text.lower().strip()
        
        # Long text (>500 chars) likely a full document
        if len(text) > 500:
            return "analyze_requirements"
        
        # Check for question patterns
        question_words = ["what", "how", "why", "when", "where", "explain", "clarify", "?"]
        if any(text_lower.startswith(word) for word in question_words):
            return "answer_question"
        
        # Check for test case generation request
        if any(keyword in text_lower for keyword in ["test case", "test scenario", "testing", "qa"]):
            return "generate_test_cases"
        
        # Check for conflict explanation request
        if any(keyword in text_lower for keyword in ["conflict", "contradiction", "mâu thuẫn", "explain"]):
            if any(keyword in text_lower for keyword in ["conflict", "contradiction", "mâu thuẫn"]):
                return "explain_conflicts"
        
        # Default to analyze if contains requirements keywords
        if any(keyword in text_lower for keyword in ["requirement", "user story", "srs", "specification"]):
            return "analyze_requirements"
        
        return "generic"
    
    def _analyze_requirements(self, text: str) -> Dict[str, Any]:
        """
        Analyze full SRS/User Stories document via HTTP API
        
        Args:
            text: Requirements document text
            
        Returns:
            Analysis results with conflicts, ambiguities, suggestions
        """
        try:
            if self.backend_available:
                # Estimate processing time based on text length
                # Fast method: ~30-60 seconds for most cases
                estimated_seconds = min(max(len(text) // 50, 30), 90)  # 30-90 seconds
                
                # Call backend HTTP API with optimized timeout
                response = requests.post(
                    f"{self.api_base_url}/api/analyze",
                    json={
                        "text": text,
                        "model": "gemini-2.5-flash"
                    },
                    timeout=90  # Optimized: 90 seconds (fast method should complete in 30-60s)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Store analysis_id for later use (export, history)
                    self.current_analysis_id = result.get("analysis_id")
                    self.current_document = result
                    # Add function_used metadata
                    result["function_used"] = "analyze_requirements"
                    return result
                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    return {
                        "conflicts": [],
                        "ambiguities": [],
                        "suggestions": [],
                        "error": f"API Error ({response.status_code}): {error_msg}",
                        "function_used": "error"
                    }
            else:
                # Fallback to mock response if backend unavailable
                mock_result = self._get_mock_analysis_result(text)
                mock_result["function_used"] = "analyze_requirements"
                return mock_result
        except requests.exceptions.Timeout:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": "⏱️ Timeout: Phân tích mất quá 90 giây. Vui lòng thử với text ngắn hơn hoặc chia nhỏ document.",
                "function_used": "error"
            }
        except requests.exceptions.ConnectionError:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"Cannot connect to backend API at {self.api_base_url}. Please ensure the backend server is running on port 8000.",
                "function_used": "error"
            }
        except Exception as e:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"Error: {str(e)}",
                "function_used": "error"
            }
    
    def _answer_question(self, text: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Answer questions about requirements using context
        
        Args:
            text: Question text
            context: Current document context
            
        Returns:
            Answer with metadata
        """
        # For now, return a simple answer
        # In the future, this would use RAG or the LLM with context
        if context and self.current_document:
            # Extract relevant information from context
            answer = f"I can answer questions about your requirements document. "
            
            if self.current_document.get("conflicts"):
                answer += f"I found {len(self.current_document['conflicts'])} conflicts. "
            if self.current_document.get("ambiguities"):
                answer += f"I found {len(self.current_document['ambiguities'])} ambiguities. "
            if self.current_document.get("suggestions"):
                answer += f"I have {len(self.current_document['suggestions'])} suggestions. "
            
            return {
                "message": answer + "\n\n" + text,
                "function_used": "answer_question"
            }
        else:
            return {
                "message": "I don't have any context yet. Please analyze a requirements document first by pasting it in the chat.",
                "function_used": "answer_question"
            }
    
    def _generate_test_cases(self, text: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate test cases from requirements
        
        Args:
            text: Request text
            context: Current document context
            
        Returns:
            Generated test cases
        """
        # For now, return a placeholder
        # In the future, this would use LLM to generate test cases
        message = "Test case generation is coming soon! "
        if self.current_document:
            message += f"I can generate test cases for your {len(self.current_document.get('parsed_requirements', []))} requirements."
        
        return {
            "message": message,
            "function_used": "generate_test_cases"
        }
    
    def _explain_conflicts(self, text: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Explain detected conflicts in detail
        
        Args:
            text: Request text
            context: Current document context
            
        Returns:
            Conflict explanations
        """
        if self.current_document and self.current_document.get("conflicts"):
            conflicts = self.current_document["conflicts"]
            explanations = []
            
            for i, conflict in enumerate(conflicts[:3], 1):  # Show first 3 conflicts
                req1 = conflict.get("req1", "")
                req2 = conflict.get("req2", "")
                desc = conflict.get("description", "")
                explanations.append(f"{i}. {req1} vs {req2}: {desc}")
            
            return {
                "message": "Here are the detected conflicts:\n\n" + "\n\n".join(explanations),
                "function_used": "explain_conflicts"
            }
        else:
            return {
                "message": "No conflicts detected yet. Please analyze a requirements document first.",
                "function_used": "explain_conflicts"
            }
    
    def _handle_generic_message(self, text: str) -> Dict[str, Any]:
        """
        Handle generic messages with helpful responses
        
        Args:
            text: User message
            
        Returns:
            Helpful response
        """
        greetings = ["hi", "hello", "hey", "xin chào", "chào"]
        if any(text.lower().startswith(g) for g in greetings):
            return {
                "message": "Hello! I'm your Requirements Engineering AI Assistant. I can help you:\n\n"
                          "• Analyze full SRS/User Stories documents\n"
                          "• Answer questions about requirements\n"
                          "• Generate test cases\n"
                          "• Explain detected conflicts\n\n"
                          "Just paste a document or ask me a question!",
                "function_used": "generic"
            }
        
        return {
            "message": "I'm here to help with requirements engineering. You can:\n\n"
                      "• Paste a requirements document to analyze it\n"
                      "• Ask questions about requirements\n"
                      "• Request test case generation\n"
                      "• Ask me to explain conflicts\n\n"
                      "What would you like to do?",
            "function_used": "generic"
        }
    
    def _get_mock_analysis_result(self, text: str) -> Dict[str, Any]:
        """Return mock analysis result for testing when backend is unavailable"""
        return {
            "conflicts": [
                {
                    "req1": "User must login",
                    "req2": "User can access without login",
                    "description": "Security requirement conflicts with accessibility requirement"
                },
                {
                    "req1": "System should be fast",
                    "req2": "System should support all features",
                    "description": "Performance conflicts with feature richness"
                }
            ],
            "ambiguities": [
                {
                    "req": "System should be user-friendly",
                    "issue": "User-friendly is subjective and not measurable"
                },
                {
                    "req": "Reports should be generated quickly",
                    "issue": "Quickly is vague, need specific time requirement"
                }
            ],
            "suggestions": [
                {
                    "req": "System should be user-friendly",
                    "new_version": "System should achieve 80%+ user satisfaction in usability testing"
                },
                {
                    "req": "Reports should be generated quickly",
                    "new_version": "Reports should be generated within 5 seconds for datasets up to 10,000 records"
                }
            ],
            "analysis_id": None,
            "function_used": "analyze_requirements"
        }
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get analysis history from backend API
        
        Args:
            limit: Number of history items to retrieve
            
        Returns:
            List of analysis history items
        """
        try:
            if self.backend_available:
                response = requests.get(
                    f"{self.api_base_url}/api/history",
                    params={"limit": limit},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("items", [])
            return []
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []
    
    def analyze_file(self, uploaded_file) -> Dict[str, Any]:
        """
        Analyze requirements from uploaded file via HTTP API
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Analysis results with conflicts, ambiguities, suggestions
        """
        # First check if backend is available
        try:
            health_check = requests.get(f"{self.api_base_url}/health", timeout=3)
            if health_check.status_code != 200:
                return {
                    "conflicts": [],
                    "ambiguities": [],
                    "suggestions": [],
                    "error": f"Backend không khả dụng (status: {health_check.status_code}). Vui lòng kiểm tra backend server.",
                    "function_used": "error"
                }
        except requests.exceptions.ConnectionError:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"❌ Không thể kết nối đến backend tại {self.api_base_url}. Vui lòng đảm bảo backend đang chạy trên port 8000.",
                "function_used": "error"
            }
        except Exception as e:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"❌ Lỗi kiểm tra backend: {str(e)}",
                "function_used": "error"
            }
        
        try:
            # Prepare file for upload
            files = {
                'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or 'text/plain')
            }
            data = {
                'model': 'gemini-2.5-flash'
            }
            
            # Call backend file upload API with optimized timeout
            # Fast method should complete in 60-90 seconds for most files
            response = requests.post(
                f"{self.api_base_url}/api/analyze/file",
                files=files,
                data=data,
                timeout=120  # Optimized: 120 seconds (fast method should complete in 60-90s)
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    # Store analysis_id for later use
                    self.current_analysis_id = result.get("analysis_id")
                    self.current_document = result
                    result["function_used"] = "analyze_requirements"
                    return result
                except ValueError as e:
                    return {
                        "conflicts": [],
                        "ambiguities": [],
                        "suggestions": [],
                        "error": f"❌ Lỗi parse response từ backend: {str(e)}. Response: {response.text[:200]}",
                        "function_used": "error"
                    }
            else:
                try:
                    error_detail = response.json().get("detail", response.text[:200])
                except:
                    error_detail = response.text[:200] if response.text else "Unknown error"
                return {
                    "conflicts": [],
                    "ambiguities": [],
                    "suggestions": [],
                    "error": f"❌ API Error ({response.status_code}): {error_detail}",
                    "function_used": "error"
                }
        except requests.exceptions.Timeout:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": "⏱️ Timeout: Phân tích file mất quá 120 giây. File có thể quá lớn (>5000 từ). Vui lòng thử với file nhỏ hơn.",
                "function_used": "error"
            }
        except requests.exceptions.ConnectionError:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"❌ Mất kết nối đến backend tại {self.api_base_url}. Vui lòng kiểm tra backend server.",
                "function_used": "error"
            }
        except Exception as e:
            return {
                "conflicts": [],
                "ambiguities": [],
                "suggestions": [],
                "error": f"❌ Lỗi: {str(e)}",
                "function_used": "error"
            }
    
    def export_analysis(self, analysis_id: int, format: str = "json") -> Optional[bytes]:
        """
        Export analysis result from backend
        
        Args:
            analysis_id: ID of analysis to export
            format: Export format ("json" or "docx")
            
        Returns:
            File content as bytes, or None if error
        """
        try:
            if self.backend_available:
                response = requests.get(
                    f"{self.api_base_url}/api/export/{format}/{analysis_id}",
                    timeout=30
                )
                if response.status_code == 200:
                    return response.content
            return None
        except Exception as e:
            print(f"Error exporting analysis: {e}")
            return None


# Create a global app instance
app = Agent()

