# DEEPSEEK_USAGE.md

## Overview  
This document details the prompts, reasoning, and lessons learned when integrating the DeepSeek API to analyze and rank Sequoia portfolio companies.

## Prompt Design  
We construct a single JSON‐based prompt that provides all necessary context and requests a structured JSON response:

With `max_tokens=2000` and `temperature=0.3` to balance depth and consistency.

## Expected Response Schema  
DeepSeek should return a JSON object exactly matching this schema:


## Challenges & Solutions  

1. **Markdown Fences**  
   - _Issue:_ DeepSeek sometimes wraps JSON in triple backticks, breaking `json.loads`.  
   - _Solution:_ Strip any leading/trailing ```

2. **Token Limits**  
   - _Issue:_ Full feature sets for 20+ companies exceed token budget.  
   - _Solution:_ Reduced feature payload to essential metrics; raised `max_tokens` to 2000.

3. **Rate Limiting & Timeouts**  
   - _Issue:_ Long responses can time out on default 30s.  
   - _Solution:_ Increased timeout to 60s and added retry logic for network errors.

4. **Schema Validation**  
   - _Issue:_ Unexpected keys or missing fields in DeepSeek output.  
   - _Solution:_ After `json.loads`, validate presence of `analysis` and `rankings` keys; log and fail gracefully if schema mismatches.

## Future Enhancements  
- Implement JSON Schema validation to enforce correct response format.  
- Batch companies into groups to stay well under token limits.  
- Add fallback logic to regenerate prompts on parse errors.

