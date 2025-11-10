from tavliy import TavilyClient
from langchain_core.prompts import ChatPromptTemplate



class AINewsNode:
    """
    Initializes the AI News Node to fetch news using Tavily API
    """
    def __init__(self,llm):
        self.llm = llm
        self.tavily = TavilyClient()
        
        
        self.state = {}
        
        
    def fetch_news(self,state: dict):
        """
        Fetch AI news based on the specified Framework frequency.
        
        Args: 
            state (dict): The state dictionary containing 'frequency'
            
        Returns: 
            dict: Updated state withe 'news_data"  key conatining fetched news.
            
        """
        
        frequency = state['messages'][0].content.lower()
        
        self.state['frequency'] = frequency
        
        time_range_map = {'daily':'d','weekly': 'w', "monthly": 'm',"yearly": 'y'}
        days_map = {'daily':1, 'weekly':7, "monthly": 30,"yearly": 365}
        
        
        response = self.tavily.search(
            query = "Top Articicial Intelligencs (AI) technology news India and globaly",
            topic = "news",
            time_range = time_range_map[frequency],
            inlcude_answer = "advacnced",
            max_results =20,
            days = days_map[frequency]
            
        )
        
        state['news_data'] = response('results',[])
        self.state['news_data'] = state['news_data']
        return state
    
    
    def summarize_news(self,state: dict):
        """
        Summarize the fetched news using LLM
        
        Args:
            state (dict): The state dictionary containing 'news_data'
            
        Returns:
            dict: Updated state with 'summary' key containing summarized news.
        """
        
        news_items = state.satte['news_data']
        
        
        
       
        
        prompt_template = ChatPromptTemplate.from_template([
          
            ("system","""Summarize AI news articles into markdown format. For each item inlcude:
             - Date in **YYYY--MM--DD** format in IST timezone
             - Concise sentences summary from latest news
             - Sort news by date wise (latest first)
             - Source URL as link
             Use format:
             ### [Date]
             - [Summarize](URL)""" ),
            ("user", "Article\n{article}")
        ])
        
        artciles_url = "\n\n".join([
            f"Content: {item.get('content', '')}\nurl: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])
        
        response = self.llm.invoke(prompt_template.format( articles= artciles_url))
        state['sumamary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_results(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews{frequency}_summary.md"
        with open (filename,'w') as f:
            f.write(f"#{frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state
    