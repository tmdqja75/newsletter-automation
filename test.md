<!-- 이제 수집한 정보를 바탕으로 한국어 뉴스레터 기사를 작성하겠습니다.

--- -->

# LangChain의 DeepAgents: 복잡한 작업을 해결하는 자율 AI 에이전트의 새로운 패러다임

## 단순한 챗봇을 넘어, '깊이 생각하는' 에이전트의 등장

여러분은 AI 에이전트에게 "최신 연구 논문을 찾아서 요약하고, 그 내용을 바탕으로 보고서를 작성해줘"라고 요청했을 때 어떤 일이 일어날까요? 기존의 단순한 AI 챗봇은 한 번의 질문에 한 번의 답변만 내놓지만, [LangChain이 새롭게 출시한 DeepAgents](https://blog.langchain.com/doubling-down-on-deepagents/)는 이런 복잡한 다단계 작업을 자율적으로 수행할 수 있는 "깊이 있는 에이전트"를 만들 수 있게 해줘요.

DeepAgents는 단순히 질문에 답하는 것을 넘어, **작업 계획을 세우고, 여러 단계를 거쳐 정보를 수집하며, 중간 결과를 파일로 저장하고, 필요시 전문화된 서브 에이전트에게 작업을 위임**하는 능력을 갖춘 자율 AI 에이전트를 구축할 수 있는 Python 패키지예요.

## DeepAgents가 해결하는 문제: '얕은 에이전트'의 한계

기존의 AI 에이전트들은 한 가지 큰 문제가 있었어요. 바로 **컨텍스트 윈도우(context window) 오버플로우** 문제예요. 복잡한 작업을 수행하다 보면 대화 기록과 중간 결과물이 계속 쌓이면서 LLM이 처리할 수 있는 토큰 한도를 넘어버리는 거죠. 

[DeepAgents는 이 문제를 근본적으로 해결](https://changelog.langchain.com/announcements/deepagents-0-2-release-for-more-autonomous-agents)하기 위해 설계되었어요. 마치 사람이 메모장에 중간 결과를 적어두고 나중에 참고하듯이, DeepAgents는 **가상 파일 시스템**을 통해 중간 결과를 파일로 저장하고, 필요할 때만 불러와 사용할 수 있어요.

## LangChain vs LangGraph vs DeepAgents: 뭐가 다른 걸까?

LangChain 생태계를 처음 접하는 분들은 이 세 가지의 차이가 헷갈릴 수 있어요. [LangChain 공식 문서](https://changelog.langchain.com/announcements/deepagents-0-2-release-for-more-autonomous-agents)에 따르면 이렇게 이해하면 돼요:

- **LangGraph (에이전트 런타임)**: 결정론적 단계와 에이전트 컴포넌트를 결합한 워크플로우를 구축하는 기반 시스템. 그래프 기반 아키텍처로 루프, 조건 분기, 멀티 에이전트 협업이 가능해요.

- **LangChain (에이전트 프레임워크)**: 코어 에이전트 루프를 제공하고, 모든 프롬프트와 도구를 직접 구축할 수 있는 프레임워크예요. LangGraph 위에 구축되어 있어요.

- **DeepAgents (에이전트 하네스)**: LangChain 위에 구축된 가장 상위 레벨의 추상화로, **계획 도구, 파일 시스템, 서브 에이전트, 상세한 프롬프트를 기본 제공**하는 자율 에이전트 구축 도구예요.

쉽게 말하면, LangGraph는 엔진이고, LangChain은 프레임, DeepAgents는 완성된 자동차 같은 거예요. 바로 운전하고 싶다면 DeepAgents를 사용하면 되고, 커스터마이징이 필요하면 LangChain이나 LangGraph를 직접 사용하면 돼요.

## DeepAgents의 핵심 기능: 미들웨어 아키텍처

DeepAgents의 가장 큰 특징은 [모듈화된 미들웨어 아키텍처](https://github.com/langchain-ai/deepagents)예요. 기본적으로 다음 미들웨어들이 내장되어 있어요:

### 1. **TodoListMiddleware (작업 계획 도구)**
에이전트가 복잡한 작업을 여러 단계로 나누고, 진행 상황을 추적할 수 있게 해줘요. `write_todos` 도구를 사용해 할 일 목록을 만들고 업데이트할 수 있어요.

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    system_prompt="복잡한 연구 작업을 수행하고 보고서를 작성하세요.",
)
```

### 2. **FilesystemMiddleware (파일 시스템 접근)**
에이전트가 파일을 읽고 쓰고 편집할 수 있게 해줘요. 대용량 결과물은 자동으로 파일로 저장되어 컨텍스트 오버플로우를 방지해요. `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep` 같은 도구를 사용할 수 있어요.

[DeepAgents 0.2 버전](https://changelog.langchain.com/announcements/deepagents-0-2-release-for-more-autonomous-agents)부터는 **플러그인 가능한 백엔드 추상화**가 추가되어, 가상 파일 시스템을 원하는 스토리지 시스템(LangGraph State, LangGraph Store, 로컬 파일 시스템, S3 등)으로 교체할 수 있어요.

### 3. **SubAgentMiddleware (서브 에이전트 위임)**
복잡한 작업을 전문화된 서브 에이전트에게 위임할 수 있어요. 이를 통해 메인 에이전트의 컨텍스트를 깨끗하게 유지하면서, 특정 작업에 대해 깊이 있는 처리가 가능해요.

```python
from deepagents import create_deep_agent

research_subagent = {
    "name": "research-agent",
    "description": "심층 질문을 연구하는 데 사용됨",
    "prompt": "당신은 전문 연구원입니다",
    "tools": [internet_search],
    "model": "openai:gpt-4o"  # 선택사항: 메인 에이전트와 다른 모델 사용 가능
}

agent = create_deep_agent(subagents=[research_subagent])
```

### 4. **기타 유용한 미들웨어**
- **SummarizationMiddleware**: 컨텍스트가 170k 토큰을 초과하면 자동으로 요약
- **AnthropicPromptCachingMiddleware**: Anthropic 사용자를 위한 프롬프트 캐싱으로 비용 절감
- **HumanInTheLoopMiddleware**: 특정 작업 전 사람의 승인을 받을 수 있도록 실행 일시 중지

## 실전 활용 사례: DeepAgents로 무엇을 만들 수 있을까?

### 1. **자동화된 연구 보고서 작성**
[DataCamp의 튜토리얼](https://www.datacamp.com/tutorial/deep-agents)에서는 DeepAgents를 활용해 구직자를 위한 자동화 도구를 만드는 예시를 보여줘요. 이 시스템은:
- 이력서를 분석하고
- 관련 채용 공고를 검색하며
- 각 채용 공고에 맞는 맞춤형 커버레터를 자동 작성해요

### 2. **DeepAgents CLI: 코딩 어시스턴트**
[LangChain은 DeepAgents CLI](https://blog.langchain.com/introducing-deepagents-cli/)도 출시했어요. 이는 터미널에서 바로 사용할 수 있는 AI 코딩 어시스턴트인데, 가장 큰 특징은 **영구 메모리 시스템**이에요.

```bash
# 설치
uv pip install deepagents-cli

# 사용
deepagents --agent my-coding-assistant
```

에이전트가 프로젝트의 API 컨벤션을 한번 학습하면, `~/.deepagents/AGENT_NAME/memories/` 폴더에 저장해두고 다음 대화에서도 계속 활용할 수 있어요. 마치 진짜 팀원이 프로젝트 컨텍스트를 기억하는 것처럼요!

### 3. **멀티 모달 연구 에이전트**
[실제 사례](https://medium.com/@pankaj_pandey/deepagents-by-langchain-building-robust-multi-step-ai-agents-for-real-world-workflows-9479e5f8186a)를 보면, 금융 규제 문서를 자동으로 찾아 분석하고 핵심 포인트를 추출하는 시스템을 만들 수 있어요:
- 최신 규제 문서를 웹에서 검색
- PDF를 다운로드하고 텍스트 추출
- 핵심 변경사항 분석
- 구조화된 보고서로 정리

## 시작하기: 간단한 예제 코드

DeepAgents를 시작하는 것은 정말 간단해요. [공식 문서](https://docs.langchain.com/oss/python/deepagents/quickstart)의 예제를 보면:

```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent

# 웹 검색 도구 설정
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """웹 검색을 수행합니다"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# Deep Agent 생성
research_instructions = """당신은 전문 연구원입니다. 
철저한 연구를 수행하고, 세련된 보고서를 작성하세요."""

agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=research_instructions
)

# 사용
result = agent.invoke({
    "messages": [{"role": "user", "content": "LangGraph가 뭐야?"}]
})
```

이렇게 몇 줄의 코드만으로 복잡한 연구 작업을 수행할 수 있는 자율 에이전트가 완성돼요!

## 마치며: AI 에이전트의 미래

DeepAgents는 단순히 새로운 라이브러리가 아니라, **AI 에이전트가 나아가야 할 방향**을 제시하고 있어요. 단편적인 질의응답을 넘어, 복잡한 다단계 작업을 자율적으로 계획하고 실행할 수 있는 "진짜 에이전트"를 만들 수 있게 된 거죠.

특히 LangGraph라는 탄탄한 런타임 위에 구축되어 있기 때문에, [LangGraph Studio로 시각화하고, LangGraph Cloud로 프로덕션 배포](https://context7.com/langchain-ai/deepagents/llms.txt)하는 것도 가능해요. 프로토타입부터 실제 서비스까지 커버할 수 있는 완성도 높은 솔루션이라고 볼 수 있어요.

AI 에이전트를 구축하고 싶다면, 이제 선택지가 명확해졌어요:
- **빠른 프로토타입과 복잡한 자율 작업**이 필요하다면 → **DeepAgents**
- **커스텀 워크플로우와 세밀한 제어**가 필요하다면 → **LangChain**
- **복잡한 상태 관리와 그래프 기반 로직**이 필요하다면 → **LangGraph**

여러분은 어떤 에이전트를 만들어보고 싶으신가요? 🤖

---

**참고 자료:**
- [LangChain 공식 블로그 - Doubling down on DeepAgents](https://blog.langchain.com/doubling-down-on-deepagents/)
- [DeepAgents 0.2 릴리즈 노트](https://changelog.langchain.com/announcements/deepagents-0-2-release-for-more-autonomous-agents)
- [DeepAgents GitHub 저장소](https://github.com/langchain-ai/deepagents)
- [DeepAgents CLI 소개](https://blog.langchain.com/introducing-deepagents-cli/)
- [LangChain 공식 문서 - DeepAgents Quickstart](https://docs.langchain.com/oss/python/deepagents/quickstart)
