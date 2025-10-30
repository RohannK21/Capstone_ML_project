import React, { useState, useRef } from "react";
import "./App.css";

export default function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const infoRef = useRef(null);

  const handlePredict = async () => {
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "Something went wrong" });
    } finally {
      setLoading(false);
    }
  };

  const handleScroll = () => {
    infoRef.current.scrollIntoView({ behavior: "smooth" });
  };

  // Determine container style
  const containerClass = result
    ? result.prediction === "SAFE"
      ? "container safe-glow"
      : "container danger-glow"
    : "container";

  return (
    <div className="main">
      {/* Landing / Prediction Section */}
      <section className={containerClass}>
      <h3 className="webcheck-title">Web Checker</h3>

        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button id="checkButton" onClick={handlePredict} disabled={loading}>
          {loading ? "Checking..." : "Check"}
        </button>

        {loading && <div className="loader"></div>}

        {result && (
          <div>
            {result.error ? (
              <p>{result.error}</p>
            ) : (
              <p>
                <strong>{result.url}</strong> is{" "}
                {result.prediction === "SAFE" ? "SAFE ✅" : "MALICIOUS ⚠️"} (
                {result.confidence}% confidence)
              </p>
            )}
          </div>
        )}

        {/* Bottom-right button */}
        <button className="scroll-btn" onClick={handleScroll}>
          How This Works ↓
        </button>
      </section>

      {/* Info Section */}
<section className="info-container" ref={infoRef}>
  <h3>How This Website Works</h3>
  <p>
    <strong>Model Utilized:</strong> This project uses a <b>Random Forest Classifier</b> (<code>sklearn.ensemble.RandomForestClassifier</code>) to detect malicious websites. Random Forest is an ensemble learning algorithm that builds multiple decision trees and combines their outputs to improve prediction accuracy and robustness.
  </p>
  <p><b>The training process involved the following steps:</b></p>
  <ul>
    <li>500 legitimate websites were randomly selected from the Alexa Top 1 Million list.</li>
    <li>500 malicious/phishing websites were sourced from a Kaggle dataset.</li>
    <li>For each URL, SSL certificate data, WHOIS information, and top-level domain (TLD) details were extracted.</li>
    <li>The extracted features were used to train the Random Forest model to classify websites as safe or malicious.</li>
    <li>Random Forest was chosen because it performs well on structured tabular data with both numerical and categorical features, handles non-linear relationships effectively, and is less prone to overfitting compared to single decision trees.</li>
  </ul>
</section>

      {/* Footer */}
<footer className="footer">
  <p className="footer-text">
    Capstone project ML — Saniya Wanjari, Saie Amdhare, Rohan Keshkar
  </p>
  <a
    href="https://github.com/RohannK21/Capstone_ML_project"
    target="_blank"
    rel="noopener noreferrer"
    className="github-link"
  ><u>
    GitHub</u>
  </a>
</footer>
    </div>
  );
}
