from typing import List, Set


def get_topics_from_classifiers_str(classifiers: str) -> List[str]:
    """
    Parses classifiers of the format Topic :: Internet :: WWW/HTTP :: WSGI :: Application
    into e.g. ["Internet", "WWW/HTTP", "WSGI", "Application"]
    """
    return get_topics_from_classifiers(
        [
            topic_classifier
            for topic_classifier in classifiers.split("\n")
            if topic_classifier
        ]
    )


def get_topics_from_classifiers(classifiers: List[str]) -> List[str]:
    """
    Parses classifiers of the format Topic :: Internet :: WWW/HTTP :: WSGI :: Application
    into e.g. ["Internet", "WWW/HTTP", "WSGI", "Application"]
    """
    topics: Set[str] = set()
    for classifier in classifiers:
        if _is_topic_classifier(classifier):
            topics.update(_get_topics_from_classifier(classifier))
    return list(topics)


def _is_topic_classifier(classifier: str) -> bool:
    return classifier.startswith("Topic ::")


def _get_topics_from_classifier(classifier: str) -> List[str]:
    """
    Parses classifiers of the format Topic :: Internet :: WWW/HTTP :: WSGI :: Application
    into e.g. ["Internet", "WWW/HTTP", "WSGI", "Application"]
    """
    topics = classifier.split(" :: ")
    if len(topics) < 2:
        return []
    return topics[1:]
