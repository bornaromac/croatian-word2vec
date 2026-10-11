# Croatian Word2Vec: Training and Evaluation

## Overview

This project investigates the training and quantitative evaluation of Word2Vec word embeddings for the Croatian language. The primary objective is to analyze how well different Word2Vec architectures capture **morphological relationships in Croatian**, with a particular focus on adjective gender transformations.

Two Word2Vec architectures were trained and compared:

- **CBOW (Continuous Bag of Words)**
- **Skip-gram**

The models were evaluated using a custom analogy benchmark, vector-offset analysis, cosine similarity, and Spearman rank correlation. The project explores how the consistency of a linguistic relationship within the embedding space affects analogy accuracy.

## Dataset

The models were trained on the **hrWaC Croatian web corpus**.

- **Corpus:** hrWaC 2.1
- **Source file:** `hrWaC2.1.01.xml.gz`
- **Source:** [CLARIN.SI Repository — hrWaC](https://www.clarin.si/repository/xmlui/handle/11356/1064)

The corpus provides a large collection of Croatian-language web texts for learning distributional word representations.

### Text preprocessing

The preprocessing pipeline included:

- Word-level tokenization
- Removal of unnecessary characters
- Text standardization
- Vocabulary filtering based on minimum word frequency

Several `min_count` configurations were explored, including 100, 50, and 20. The final configuration used **`min_count = 20`** as a practical compromise between vocabulary coverage, noise reduction, memory consumption, and computational cost.

## Model Training

Two Word2Vec architectures were trained using the same baseline hyperparameters to enable comparison.

| Parameter | Value |
|---|---:|
| Vector size | 300 |
| Context window | 7 |
| Minimum word frequency (`min_count`) | 20 |
| Negative sampling | 5 |
| Training epochs | 15 |
| CBOW configuration (`sg`) | 0 |
| Skip-gram configuration (`sg`) | 1 |

Multiple experiments were conducted with different preprocessing strategies, corpus configurations, analogy sets, and hyperparameters. Some experiments required more than 11 hours of training without producing sufficiently strong evaluation results.

The final baseline comparison was:

| Model | Overall analogy accuracy |
|---|---:|
| CBOW | 0.71 |
| Skip-gram | 0.62 |

In these experiments, CBOW outperformed Skip-gram on the selected analogy benchmark.

The trained models were saved in `.model` and `.kv` formats to support subsequent evaluation without retraining.

## Analogy Benchmark Construction

Because a suitable predefined analogy benchmark was not available for the project's specific evaluation objective, a custom evaluation set was constructed using an existing Croatian analogy resource.

**Initial resource:** [Croatian analogy dataset (cr-analogy)](https://drive.google.com/drive/folders/1gVaQ3WZNek8O4u0pGWFeXAcH1KgFiW-Y?usp=sharing)

The benchmark focused on adjective gender transformations (`adj_gender`), selected because this morphological relationship can exhibit approximately consistent directional patterns in an embedding space.

Rather than manually creating every seed pair, candidate relationships were filtered from the existing analogy resource through a multi-stage procedure.

The filtering process included:

1. Identifying productive masculine-to-feminine adjective patterns.
2. Automatically generating candidate pairs and checking vocabulary coverage.
3. Removing out-of-vocabulary words.
4. Filtering nouns and inflected forms that did not match the intended relationship.
5. Checking semantic and morphological consistency.

The objective was to construct a benchmark with a clear linguistic interpretation and a sufficiently consistent relationship for quantitative evaluation.

## Vector Offset Analysis

Word analogies can be evaluated by examining relationships between word vectors.

For a relationship represented by a source pair, the vector offset is calculated as:

\[
\Delta = \mathbf{v}_{\text{target}}-\mathbf{v}_{\text{source}}
\]

For example, if the relationship is a masculine-to-feminine transformation, the corresponding vector offsets can be compared across multiple adjective pairs.

Cosine similarity was used to investigate how consistently these offsets pointed in similar directions in the embedding space.

The analysis indicated that consistency varied across word pairs. Some pairs represented the intended morphological relationship more reliably than others, motivating a systematic evaluation of the benchmark's composition.

## Evaluation Set Optimization

An empirical sweep was performed using a parameter named `KEEP`, which controlled how many of the most consistent pairs were retained for evaluation.

The analysis showed that including more pairs tended to reduce the overall consistency of the target morphological relationship.

A value of **`KEEP = 80`** was selected as a compromise between benchmark size, relationship consistency, and representativeness.

Importantly, **the Word2Vec model was not retrained during this optimization step**. The learned vectors remained unchanged; only the evaluation set was modified through the consistency-based filtering procedure.

This distinction is essential when interpreting the final results.

## Final Results

The selected evaluation configuration produced the following result:

| Evaluation component | Result |
|---|---:|
| Selected `KEEP` value | 80 |
| Number of analogy questions | 3,160 |
| Final analogy accuracy | **91.68%** |
| Spearman correlation between human similarity ratings and vector cosine similarity | Approximately 0.17 |

The final analogy accuracy reflects performance on the filtered evaluation set. It should not be interpreted as a general measure of performance across all Croatian words, morphological categories, or unrestricted analogy tasks.

### Human similarity comparison

Spearman's rank correlation was calculated between human similarity ratings and cosine similarities derived from the word vectors.

The observed correlation of approximately **0.17** indicates a weak positive association between the two rankings.

This result illustrates that strong performance on a structured morphological analogy task does not necessarily imply equally strong agreement with human judgments of general semantic similarity.

Potential contributing factors include the morphological complexity of Croatian, the relatively limited evaluation set, and the use of a model trained without lemmatization.

### Linear analogy example

The project also explored analogies based on linear relationships between word vectors, following the general form:

\[
\mathbf{v}_{\text{king}}-\mathbf{v}_{\text{man}}
+\mathbf{v}_{\text{woman}}
\approx \mathbf{v}_{\text{queen}}
\]

This illustrates the vector-offset principle underlying traditional Word2Vec analogy evaluation.

## Key Findings

- CBOW achieved higher baseline analogy accuracy than Skip-gram on the selected benchmark.
- The consistency of a morphological relationship within the embedding space had a substantial effect on analogy evaluation.
- Filtering analogy pairs by relationship consistency improved the final benchmark result without retraining or modifying the learned embeddings.
- The final evaluation achieved 91.68% accuracy on 3,160 analogy questions.
- The weak positive Spearman correlation suggests that performance on morphological analogies and agreement with human similarity judgments measure different aspects of word representation quality.

## Technical Decisions and Limitations

### Evaluation-set composition

The final result depends on the composition and filtering of the analogy benchmark. The selected score demonstrates performance on a deliberately structured set of morphological relationships, rather than general-purpose language understanding.

### Morphological variability

Croatian has a rich morphological system. Gender transformations may be affected by lexical exceptions, ambiguous forms, inflection, and variation in how consistently a relationship is represented in the embedding space.

### No lemmatization

The final configuration did not use lemmatization. Although this simplified the preprocessing pipeline, it may have affected the consistency of word representations across morphological forms.

### Benchmark scope

The evaluation focused primarily on adjective gender transformations. Further evaluation would be required to assess syntactic, semantic, and other morphological relationships.

### Model comparison

The reported CBOW and Skip-gram scores apply to the selected baseline configuration and benchmark. They should not be interpreted as a universal ranking of the two Word2Vec architectures.


## Conclusion

This project demonstrates an experimental workflow for training and evaluating Croatian word embeddings, with a focus on morphological analogy relationships.

The results highlight the importance of linguistic consistency in benchmark construction and show that analogy accuracy depends not only on the trained embeddings but also on how the evaluation task is defined.

The final score of 91.68% represents performance on the selected consistency-filtered analogy benchmark and provides a starting point for further investigation of Croatian word representations.

