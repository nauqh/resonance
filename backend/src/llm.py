from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import os

load_dotenv()


class LLM():
    def __init__(self, key) -> None:
        self.llm = ChatOpenAI(
            openai_api_key=key, model="gpt-4-1106-preview")

    def __get_parser(self):
        schema = [
            ResponseSchema(
                name='genre', description="The name of the genre"),
            ResponseSchema(
                name='mood', description="List of three adjectives that describe the mood of the genre"),
            ResponseSchema(
                name='color', description="The hex color code for a color that matches the mood"),
            ResponseSchema(
                name='characteristics', description="List of two paragraphs"),
            ResponseSchema(
                name='artists', description="List of two artist names"),
            ResponseSchema(
                name='content', description="List of two description of these artists music style ")]
        return StructuredOutputParser.from_response_schemas(schema)

    def __get_context(self):
        context = """You are a music recommendation system that analyzes user music taste and 
                recommend artists and songs that align with their genre. You will be provided 
                with a genre name or a description of a kind of music, and your task are:
                    - Define the genre name of the provided description 
                    - Generate three adjectives that describe the mood of the genre
                    - Generate the hex color code for a color that matches the mood
                    - Generate 2 short paragraphs (total 100 words) that describe the characteristics of the genre. The first paragraph will begins with the phrase "Your music taste leans a bit towards <genre>"
                    or similar.
                    - Give the names of 2 trending artists for the genre
                    - Give a short description of these artists music style. Each paragraph has to
                    start with "is" as it referred to the artist name.
                Write your output in json format with sample response:
                    genre: 'Indie Folk'
                    mood: 'uplifting - harmonious - lyrical'
                    color: '#1a237e'
                    characteristics: [
                            "Your music taste leans a bit towards Indie Folk, characterized by its melodic simplicity and heartfelt lyrics. Typical representation of this taste encompass acoustic instruments like guitars, banjos, and harmonicas, often accompanied by soft, emotive vocals.",
                            "This genre tends to strike a balance between melancholic and uplifting tones, offering a mix of introspective, soul-searching ballads and cheerful, foot-tapping tunes. The tempo is generally moderate, allowing for a comfortable sway between introspection and celebration. Indie Folk resonates with a raw, organic quality, inviting listeners to connect with its unfiltered emotions."]
                    artists: ['Imagine Dragons, Charlie Puth]
                    content:[
                        "is known for their energetic and anthemic sound, characterized by powerful vocals, dynamic instrumentals, a fusion of rock, pop, and electronic elements. Their music often features catchy melodies, impactful choruses, and introspective lyrics, creating distinctive and widely appealing sonic signature.",
                        "is renowned for his emotive voice and romantic ballads, often accompanied by lush acoustic instrumentation. His music is deeply rooted in Vietnamese culture, yet it has a modern flair that makes it accessible to a wider audience, both locally and internationally."
                    ]
                """
        return context

    def analyze(self, genre: str):
        prompt = ChatPromptTemplate.from_messages([("system"), self.__get_context(),
                                                   ("human"), "{genre}"])

        chain = prompt | self.llm
        result = chain.invoke({'genre': genre})

        return self.__get_parser().parse(result.content)


if __name__ == "__main__":
    x = LLM(os.environ['API_KEY']).analyze("Korean Pop Indie")
    print(x)
