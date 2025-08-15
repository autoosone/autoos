from crewai import Agent, Crew, Task
# from crewai_tools import SerperDevTool  # Temporarily disabled
from langchain_openai import ChatOpenAI


async def agent():
    # Vehicle search and analysis agent
    # search_tool = SerperDevTool()  # Temporarily disabled
    search_tool = []  # No tools for now
    
    vehicle_expert = Agent(
        role="Automotive Expert",
        goal="Find and analyze vehicles that match customer requirements",
        backstory="""You are an experienced automotive expert with deep knowledge of:
        - All major car brands and models
        - Vehicle specifications and features
        - Market pricing and value analysis
        - Fuel efficiency and performance metrics
        - Safety ratings and reliability scores
        - Common issues and maintenance costs
        
        You help customers find the perfect vehicle by understanding their needs,
        budget, and preferences. You provide honest, unbiased recommendations.""",
        tools=search_tool,  # Empty list for now
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        verbose=True,
    )
    
    pricing_analyst = Agent(
        role="Automotive Pricing Analyst",
        goal="Analyze vehicle pricing and market trends",
        backstory="""You are a pricing specialist who tracks:
        - Current market values
        - Historical pricing trends
        - Seasonal price variations
        - Regional price differences
        - Depreciation rates
        - Best times to buy
        
        You help customers understand if they're getting a good deal.""",
        tools=search_tool,  # Empty list for now
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        verbose=True,
    )
    
    # Define tasks
    search_task = Task(
        description="""Search for vehicles based on customer requirements:
        {request}
        
        Consider:
        - Budget constraints
        - Vehicle type (SUV, sedan, truck, etc.)
        - Fuel efficiency requirements
        - Size and seating needs
        - Features and technology
        - Brand preferences
        
        Provide top 3-5 matching vehicles with:
        - Make, model, year
        - Price range
        - Key specifications
        - Pros and cons
        - Why it matches their needs
        """,
        agent=vehicle_expert,
        expected_output="Detailed vehicle recommendations with specifications and reasoning",
    )
    
    pricing_task = Task(
        description="""Analyze pricing for recommended vehicles:
        
        For each vehicle:
        - Current market price range
        - Fair purchase price
        - Expected depreciation
        - Comparison to similar models
        - Best deals available
        - Financing estimates (if budget provided)
        """,
        agent=pricing_analyst,
        expected_output="Comprehensive pricing analysis with recommendations",
    )
    
    # Create and return crew
    crew = Crew(
        agents=[vehicle_expert, pricing_analyst],
        tasks=[search_task, pricing_task],
        verbose=True,
    )
    
    return crew
