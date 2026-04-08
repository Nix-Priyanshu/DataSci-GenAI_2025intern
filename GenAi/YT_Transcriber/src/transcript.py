def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Look for manual English, then generated English
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            transcript = transcript_list.find_generated_transcript(['en'])
            
        data = transcript.fetch()
        return " ".join([i['text'] for i in data])
    except Exception as e:
        return None
