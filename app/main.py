from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI


def invoke_llm(prompt:str, context: str, criteria: str):

    template = "Question: {question}"

    prompt_template = PromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o", temperature=0)


    llm_chain = prompt_template | llm

    question = f"""You are a virtual real estate agent who provided comparison of properties based on the question an criteria a user provides.
    This is the user input: {prompt}
    A vector database has been created to store the data of the properties. And pulled context based on user input.
    This is the context: {context}
    What is the best property among the provided results and why. Please format the results neatly. Use html tags for your entire response. Use tables if necessary."""

    answer = llm_chain.invoke(question)

    return str(answer.content)

# if __name__ == "__main__":
#     prompt = "get me houses in Puerto Rico"
#     context = "Houses in Puerto Rico"
#     criteria = "best property"
#     response = invoke_llm(prompt, context, criteria)
#     print(response)


