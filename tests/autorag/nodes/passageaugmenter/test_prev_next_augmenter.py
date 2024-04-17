from autorag.nodes.passageaugmenter import prev_next_augmenter

from tests.autorag.nodes.passageaugmenter.test_base_passage_augmenter import ids_list, all_ids_list, project_dir, \
    previous_result, corpus_data


def test_prev_next_augmenter_next():
    results = prev_next_augmenter.__wrapped__(ids_list, all_ids_list, num_passages=1, mode='next')
    assert results == [['2', '3'], ['3', '4'], ['0', '1', '6']]


def test_prev_next_augmenter_prev():
    results = prev_next_augmenter.__wrapped__(ids_list, all_ids_list, num_passages=1, mode='prev')
    assert results == [['1', '2'], ['2', '3'], ['0', '5', '6']]


def test_prev_next_augmenter_both():
    results = prev_next_augmenter.__wrapped__(ids_list, all_ids_list, num_passages=1, mode='both')
    assert results == [['1', '2', '3'], ['2', '3', '4'], ['0', '1', '5', '6']]


def test_prev_next_augmenter_multi_passages():
    results = prev_next_augmenter.__wrapped__(ids_list, all_ids_list, num_passages=3, mode='prev')
    assert results == [['0', '1', '2'], ['0', '1', '2', '3'], ['0', '3', '4', '5', '6']]


def test_prev_next_augmenter_node():
    result_df = prev_next_augmenter(project_dir=project_dir, previous_result=previous_result, mode='next')
    contents = result_df["retrieved_contents"].tolist()
    ids = result_df["retrieved_ids"].tolist()
    scores = result_df["retrieve_scores"].tolist()
    assert len(contents) == len(ids) == len(scores) == 2
    assert len(contents[0]) == len(ids[0]) == len(scores[0]) == 4
    for content_list, id_list, score_list in zip(contents, ids, scores):
        for i, (content, _id, score) in enumerate(zip(content_list, id_list, score_list)):
            assert isinstance(content, str)
            assert isinstance(_id, str)
            assert isinstance(score, float)
            assert _id in corpus_data["doc_id"].tolist()
            assert content == corpus_data[corpus_data["doc_id"] == _id]["contents"].values[0]
            if i >= 1:
                assert score_list[i - 1] >= score_list[i]
