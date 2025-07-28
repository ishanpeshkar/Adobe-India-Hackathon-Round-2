"""
Section Ranker for Challenge 1B - Persona-Driven Document Intelligence
"""

import math
from typing import Dict, List, Any
from collections import Counter


class SectionRanker:
    """Ranks document sections based on relevance and importance"""
    
    def __init__(self):
        pass
    
    def _compute_position_weight(self, section_data: Dict[str, Any]) -> float:
        """Calculate score based on section position"""
        # Earlier sections get slight bonus
        section_index = section_data.get("position", 0)
        if section_index < 3:
            return 1.0
        elif section_index < 10:
            return 0.8
        else:
            return 0.6

    def _extract_context_keywords(self, user_role: str, user_task: str) -> set:
        """Extract relevant keywords from persona and job context"""
        text_combined = f"{user_role} {user_task}".lower()
        keyword_collection = set(word for word in text_combined.split() if len(word) > 2)
        return keyword_collection

    def rank_sections(self, section_list: List[Dict[str, Any]], persona_info: Dict[str, str], task_info: Dict[str, str]) -> List[Dict[str, Any]]:
        """Rank sections by relevance to persona and job context"""
        if not section_list:
            return []
        
        # Create persona context from persona and job
        context_info = self._build_persona_context(persona_info, task_info)
        
        # Calculate scores for each section
        sorted_sections = []
        for section_item in section_list:
            score_value = self._compute_final_score(section_item, context_info)
            modified_section = section_item.copy()
            modified_section['relevance_score'] = score_value
            modified_section['final_relevance_score'] = score_value
            sorted_sections.append(modified_section)
        
        # Sort by score descending
        sorted_sections.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return sorted_sections

    def _calculate_word_frequencies(self, content_text: str) -> Counter:
        """Calculate word frequency distribution"""
        word_tokens = content_text.lower().split()
        return Counter(word_tokens)

    def _build_persona_context(self, persona_info: Dict[str, str], task_info: Dict[str, str]) -> Dict[str, Any]:
        """Build context dictionary from persona and job information"""
        return {
            "persona_role": persona_info.get("role", ""),
            "job_context": task_info.get("task", "")
        }

    def _assess_content_length(self, content_text: str) -> float:
        """Calculate score based on content length"""
        token_count = len(content_text.split())
        
        if token_count < 10:
            return 0.3  # Too short
        elif token_count < 50:
            return 0.8  # Good length
        elif token_count < 200:
            return 1.0  # Ideal length
        elif token_count < 500:
            return 0.7  # Getting long
        else:
            return 0.4  # Too long

    def _compute_tfidf_relevance(self, content_text: str, context_info: Dict[str, Any]) -> float:
        """Calculate TF-IDF based relevance score"""
        context_keywords = self._extract_context_keywords(
            context_info.get("persona_role", ""),
            context_info.get("job_context", "")
        )
        
        if not context_keywords:
            return 0.5  # Default score if no context
        
        term_frequencies = self._calculate_word_frequencies(content_text)
        word_total = len(content_text.lower().split())
        
        score_total = self._sum_keyword_scores(context_keywords, term_frequencies, word_total)
        
        return min(score_total, 1.0)

    def _sum_keyword_scores(self, keywords: set, word_freq: Counter, total_count: int) -> float:
        """Sum TF-IDF scores for all keywords"""
        total_score = 0.0
        for keyword in keywords:
            if keyword in word_freq:
                term_frequency = word_freq[keyword] / total_count
                # Simple IDF approximation
                inverse_doc_freq = math.log(1 + 1 / max(1, word_freq[keyword]))
                total_score += term_frequency * inverse_doc_freq
        
        return total_score

    def _compute_final_score(self, doc_section: Dict[str, Any], context_data: Dict[str, Any]) -> float:
        """Calculate composite relevance score"""
        section_content = doc_section.get("content", "")
        if not section_content:
            return 0.0
        
        # TF-IDF based scoring
        semantic_score = self._compute_tfidf_relevance(section_content, context_data)
        
        # Length penalty (very short or very long sections get lower scores)
        length_weight = self._assess_content_length(section_content)
        
        # Position bonus (earlier sections might be more important)
        position_weight = self._compute_position_weight(doc_section)
        
        # Combine scores
        final_score = (0.6 * semantic_score + 0.3 * length_weight + 0.1 * position_weight)
        
        return min(final_score, 1.0)
