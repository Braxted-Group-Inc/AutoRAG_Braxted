from autorag.evaluator import Evaluator



if __name__ == '__main__':
    evaluator = Evaluator(qa_data_path='dedupe_qa.parquet', corpus_data_path='dedupe_question_corpus.parquet')
    evaluator.start_trial('question_match_test.yaml')