from scipy.special import expit

score = 2.5997362  # top reranker score

confidence = expit(score)

print("Confidence:", confidence)

if confidence < 0.35:
    print("Fallback")
else:
    print("Generate answer")