from .tools.rag_product_search import RAGProductSearchTool
from .intent import is_product_query

class VoicePipeline:
    def __init__(self, stt, llm, tts):
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.rag_tool = RAGProductSearchTool()

    async def handle_audio_turn(self, audio_bytes: bytes):
        # Step 1: STT
        transcript = self.stt.transcribe(audio_bytes)

        rag_results = None

        # Step 2: Check if product question
        if is_product_query(transcript):
            try:
                rag_results = await self.rag_tool.run(transcript)
            except Exception as e:
                print("RAG tool error:", e)

        # Step 3: Build LLM prompt
        prompt = f"User said: {transcript}\n"

        if rag_results:
            prompt += f"\nHere are matching products:\n{rag_results}\n"
        else:
            prompt += "\nNo matching products found or not a product query.\n"

        # Step 4: Call LLM
        reply_text = await self.llm.chat(prompt)

        # Step 5: Convert to audio
        reply_audio = self.tts.synthesize(reply_text)

        return {
            "user_transcript": transcript,
            "assistant_reply_text": reply_text,
            "assistant_reply_audio": reply_audio,
            "rag_results": rag_results,
        }
