from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_watch_history, preprocess_subscriptions, create_combined_table


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_watch_history,
                inputs="watch_history",
                outputs="preprocessed_watch_history",
                name="preprocess_watch_history_node",
            ),
            node(
                func=preprocess_subscriptions,
                inputs="subscriptions",
                outputs="preprocessed_subscriptions",
                name="preprocess_subscriptions_node",
            ),
            node(
                func=create_combined_table,
                inputs=["preprocessed_watch_history","preprocessed_subscriptions"],
                outputs="combined_table",
                name="combine_table_node",
            ),
        ]
    )
