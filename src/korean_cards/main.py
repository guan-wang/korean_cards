import os
from dotenv import load_dotenv
from crew import KoreanTutorCrew
load_dotenv(override=True)

def main():
    print("🤖 Booting up Korean Tutor (Iteration 1)...")
    tutor = KoreanTutorCrew()
    
    # Test Text: Climate change is significantly affecting Korean society. Many people are worried about environmental issues, and the government is looking for solutions.
    text = "기후 변화가 한국 사회에 큰 영향을 미치고 있습니다. 많은 사람들이 환경 문제를 걱정하고 있으며, 정부가 해결책을 찾고 있습니다." 
    
    # --- PHASE 1: ANALYSIS ---
    print(f"\n🔍 Analyzing: {text}")
    tutor.run_tutor(korean_text=text)

if __name__ == "__main__":
    main()