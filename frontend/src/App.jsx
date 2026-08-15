import { useState } from "react";
import "./App.css";


// ============================================================
// API CONFIGURATION
// ============================================================

const API_URL = "http://127.0.0.1:8000";


// ============================================================
// AVAILABLE DOCUMENTS
// ============================================================

const DOCUMENT_OPTIONS = [
  "Driving License",
  "PAN Card",
  "Vehicle Registration",
  "Vehicle Insurance",
  "Challan",
  "Vehicle Tax Receipt",
  "Vehicle Fitness Certificate",
  "Form 16",
  "TDS Certificate",
  "ePAN",
  "Passport",
  "Health Card",
  "PMJAY",
  "Health Fitness Certificate",
  "Health Policy",
  "COVID Vaccine Certificate",
  "National Health ID",
  "Health Insurance",
  "UAN Card",
  "ePRAN Card",
  "Pension Certificate",
  "Ration Card",
  "APAAR",
  "Class 10 Marksheet",
  "Class 10 Passing Certificate",
  "Class 10 Migration Certificate",
  "Class 10 School Leaving Certificate",
  "Class 12 Marksheet",
  "Class 12 Passing Certificate",
  "Class 12 Migration Certificate",
  "Class 1-9 Marksheets",
  "Degree Certificate",
  "Provisional Degree",
  "Diploma Certificate",
  "Bonafide Certificate",
  "Caste Certificate",
  "Income Certificate",
  "Birth Certificate",
  "CKYC Card"
];


// ============================================================
// MAIN APP
// ============================================================

function App() {

  // ==========================================================
  // USER FORM
  // ==========================================================

  const [form, setForm] = useState({

    age: 22,

    occupation: "Student",

    state: "Delhi",

    vehicle_owner: true,

    taxpayer: true,

    student: true,

    existing_documents: [
      "Driving License",
      "PAN Card"
    ],

    query: "I bought a bike"
  });


  // ==========================================================
  // RECOMMENDATIONS
  // ==========================================================

  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [showDocuments, setShowDocuments] = useState(false);


  // ==========================================================
  // HANDLE NORMAL INPUT
  // ==========================================================

  const handleChange = (event) => {

    const {
      name,
      value
    } = event.target;

    setForm(
      previous => ({
        ...previous,
        [name]: value
      })
    );
  };


  // ==========================================================
  // HANDLE CHECKBOX
  // ==========================================================

  const handleCheckbox = (event) => {

    const {
      name,
      checked
    } = event.target;

    setForm(
      previous => ({
        ...previous,
        [name]: checked
      })
    );
  };


  // ==========================================================
  // HANDLE EXISTING DOCUMENT
  // ==========================================================

  const handleDocumentToggle = (document) => {

    setForm(
      previous => {

        const exists =
          previous.existing_documents.includes(
            document
          );

        let documents;

        if (exists) {

          documents =
            previous.existing_documents.filter(
              item => item !== document
            );

        } else {

          documents = [
            ...previous.existing_documents,
            document
          ];
        }

        return {
          ...previous,
          existing_documents: documents
        };
      }
    );
  };


  // ==========================================================
  // GET RECOMMENDATIONS
  // ==========================================================

  const getRecommendations = async () => {

    setLoading(true);

    setError("");

    setRecommendations([]);


    try {

      const response = await fetch(
        `${API_URL}/recommend`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            age: Number(form.age),

            occupation: form.occupation,

            state: form.state,

            vehicle_owner:
              Boolean(form.vehicle_owner),

            taxpayer:
              Boolean(form.taxpayer),

            student:
              Boolean(form.student),

            existing_documents:
              form.existing_documents,

            query:
              form.query

          })
        }
      );


      if (!response.ok) {

        let message =
          `Server error: ${response.status}`;

        try {

          const errorData =
            await response.json();

          if (errorData.detail) {

            message =
              typeof errorData.detail === "string"
                ? errorData.detail
                : JSON.stringify(
                    errorData.detail
                  );
          }

        } catch {

          // Ignore JSON parsing errors

        }

        throw new Error(message);
      }


      const data =
        await response.json();


      console.log(
        "Recommendation API response:",
        data
      );


      if (
        data.status &&
        data.status !== "success"
      ) {

        throw new Error(
          "Recommendation service returned an unsuccessful response."
        );
      }


      setRecommendations(
        data.recommendations || []
      );


      if (
        !data.recommendations ||
        data.recommendations.length === 0
      ) {

        setError(
          "No recommendations were found for this query."
        );
      }

    }

    catch (err) {

      console.error(
        "Recommendation error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to the recommendation server."
      );

    }

    finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // FORMAT SCORE
  // ==========================================================

  const formatScore = (
    score,
    capAt100 = true
  ) => {

    const numericScore =
      Number(score) || 0;

    let percentage =
      numericScore * 100;


    if (capAt100) {

      percentage =
        Math.max(
          0,
          Math.min(
            100,
            percentage
          )
        );
    }


    return percentage.toFixed(1);
  };


  // ==========================================================
  // GET DOCUMENT ICON
  // ==========================================================

  const getIcon = (document) => {

    const name =
      document.toLowerCase();


    if (
      name.includes("vehicle") ||
      name.includes("driving") ||
      name.includes("challan")
    ) {

      return "🚗";
    }


    if (
      name.includes("pan") ||
      name.includes("tax") ||
      name.includes("tds") ||
      name.includes("form 16") ||
      name.includes("financial")
    ) {

      return "💰";
    }


    if (
      name.includes("degree") ||
      name.includes("student") ||
      name.includes("class") ||
      name.includes("education") ||
      name.includes("bonafide") ||
      name.includes("apaar")
    ) {

      return "🎓";
    }


    if (
      name.includes("health") ||
      name.includes("vaccine") ||
      name.includes("pmjay") ||
      name.includes("medical")
    ) {

      return "🏥";
    }


    if (
      name.includes("passport") ||
      name.includes("birth") ||
      name.includes("identity") ||
      name.includes("ckyc")
    ) {

      return "🪪";
    }


    if (
      name.includes("insurance")
    ) {

      return "🛡️";
    }


    return "📄";
  };


  // ==========================================================
  // GET SCORE CLASS
  // ==========================================================

  const getScoreClass = (score) => {

    const value =
      Number(score) || 0;


    if (value >= 0.8) {

      return "score-high";
    }


    if (value >= 0.6) {

      return "score-medium";
    }


    return "score-low";
  };


  // ==========================================================
  // CLEAR RESULTS
  // ==========================================================

  const clearResults = () => {

    setRecommendations([]);

    setError("");
  };


  // ==========================================================
  // RENDER
  // ==========================================================

  return (

    <div className="app">


      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div className="header-content">

          <div>

            <div className="logo">

              DigiLocker

              <span>AI</span>

            </div>

            <p className="subtitle">

              Intelligent Document Recommendation System

            </p>

          </div>


          <div className="header-status">

            <span className="status-dot"></span>

            AI Engine Active

          </div>

        </div>

      </header>


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="container">


        {/* ====================================================
            PROFILE CARD
        ==================================================== */}

        <section className="profile-card">


          <div className="section-title">

            <div>

              <div className="section-label">
                PERSONALIZATION
              </div>

              <h2>
                Your Profile
              </h2>

              <p>
                Tell us about yourself to get
                personalized document recommendations.
              </p>

            </div>

          </div>


          {/* ==================================================
              BASIC INFORMATION
          ================================================== */}

          <div className="form-grid">


            {/* AGE */}

            <div className="form-group">

              <label>
                Age
              </label>

              <input
                type="number"
                name="age"
                min="1"
                max="120"
                value={form.age}
                onChange={handleChange}
              />

            </div>


            {/* OCCUPATION */}

            <div className="form-group">

              <label>
                Occupation
              </label>

              <select
                name="occupation"
                value={form.occupation}
                onChange={handleChange}
              >

                <option>
                  Student
                </option>

                <option>
                  Employee
                </option>

                <option>
                  Business Owner
                </option>

                <option>
                  Government Employee
                </option>

                <option>
                  Self Employed
                </option>

                <option>
                  Other
                </option>

              </select>

            </div>


            {/* STATE */}

            <div className="form-group">

              <label>
                State
              </label>

              <input
                type="text"
                name="state"
                value={form.state}
                onChange={handleChange}
                placeholder="Enter your state"
              />

            </div>


          </div>


          {/* ==================================================
              PROFILE OPTIONS
          ================================================== */}

          <div className="checkbox-container">


            <label className="checkbox-item">

              <input
                type="checkbox"
                name="student"
                checked={form.student}
                onChange={handleCheckbox}
              />

              <span>
                🎓 I am a student
              </span>

            </label>


            <label className="checkbox-item">

              <input
                type="checkbox"
                name="vehicle_owner"
                checked={form.vehicle_owner}
                onChange={handleCheckbox}
              />

              <span>
                🚗 I own a vehicle
              </span>

            </label>


            <label className="checkbox-item">

              <input
                type="checkbox"
                name="taxpayer"
                checked={form.taxpayer}
                onChange={handleCheckbox}
              />

              <span>
                💰 I am a taxpayer
              </span>

            </label>


          </div>


          {/* ==================================================
              EXISTING DOCUMENTS
          ================================================== */}

          <div className="documents-section">

            <div className="documents-header">

              <div>

                <label>
                  Existing Documents
                </label>

                <p>
                  Select documents you already have.
                </p>

              </div>


              <button
                type="button"
                className="document-toggle"
                onClick={() =>
                  setShowDocuments(
                    !showDocuments
                  )
                }
              >

                {showDocuments
                  ? "Hide Documents"
                  : "Select Documents"
                }

              </button>

            </div>


            {/* SELECTED DOCUMENTS */}

            <div className="selected-documents">

              {form.existing_documents.length === 0 ? (

                <span className="no-documents">

                  No documents selected

                </span>

              ) : (

                form.existing_documents.map(
                  document => (

                    <span
                      className="document-chip"
                      key={document}
                    >

                      {getIcon(document)}

                      {document}

                      <button
                        type="button"
                        onClick={() =>
                          handleDocumentToggle(
                            document
                          )
                        }
                      >
                        ×
                      </button>

                    </span>

                  )
                )

              )}

            </div>


            {/* DOCUMENT SELECTION */}

            {showDocuments && (

              <div className="document-list">

                {DOCUMENT_OPTIONS.map(
                  document => (

                    <label
                      className="document-option"
                      key={document}
                    >

                      <input
                        type="checkbox"
                        checked={
                          form.existing_documents.includes(
                            document
                          )
                        }
                        onChange={() =>
                          handleDocumentToggle(
                            document
                          )
                        }
                      />

                      <span>

                        {getIcon(document)}

                        {document}

                      </span>

                    </label>

                  )
                )}

              </div>

            )}

          </div>


          {/* ==================================================
              QUERY
          ================================================== */}

          <div className="query-section">

            <label>
              What do you need?
            </label>

            <p>
              Describe what you are looking for.
            </p>

            <input
              className="query-input"
              type="text"
              name="query"
              value={form.query}
              onChange={handleChange}
              placeholder="Example: I bought a bike"
              onKeyDown={(event) => {

                if (
                  event.key === "Enter"
                ) {

                  getRecommendations();

                }

              }}
            />

          </div>


          {/* ==================================================
              ACTION BUTTONS
          ================================================== */}

          <div className="button-container">

            <button
              className="recommend-button"
              onClick={getRecommendations}
              disabled={
                loading ||
                !form.query.trim()
              }
            >

              {loading ? (

                <>
                  <span className="spinner"></span>

                  Finding Documents...

                </>

              ) : (

                <>
                  ✨ Get Recommendations
                </>

              )}

            </button>


            {recommendations.length > 0 && (

              <button
                className="clear-button"
                onClick={clearResults}
              >

                Clear Results

              </button>

            )}

          </div>


        </section>


        {/* ====================================================
            ERROR
        ==================================================== */}

        {error && (

          <div className="error">

            <span>
              ⚠️
            </span>

            <div>

              <strong>
                Something went wrong
              </strong>

              <p>
                {error}
              </p>

            </div>

          </div>

        )}


        {/* ====================================================
            LOADING
        ==================================================== */}

        {loading && (

          <section className="loading-card">

            <div className="loading-animation">

              <div className="loading-spinner"></div>

            </div>

            <h3>
              Analyzing your request...
            </h3>

            <p>
              Our AI is combining semantic search,
              document relationships and XGBoost ranking.
            </p>

          </section>

        )}


        {/* ====================================================
            RESULTS
        ==================================================== */}

        {!loading &&
          recommendations.length > 0 && (

          <section className="results-section">


            {/* ==================================================
                RESULTS HEADER
            ================================================== */}

            <div className="results-header">

              <div>

                <div className="ai-label">
                  ✨ AI RESULTS
                </div>

                <h2>
                  Recommended Documents
                </h2>

                <p>
                  Based on your profile and
                  "{form.query}"
                </p>

              </div>


              <div className="found-count">

                {recommendations.length}

                <small>
                  documents found
                </small>

              </div>

            </div>


            {/* ==================================================
                RECOMMENDATION LIST
            ================================================== */}

            <div className="recommendation-list">


              {recommendations.map(
                (recommendation, index) => {


                  const score =
                    Number(
                      recommendation.score
                    ) || 0;


                  const percentage =
                    formatScore(
                      score,
                      true
                    );


                  return (

                    <div
                      className="recommendation-card"
                      key={
                        recommendation.document ||
                        index
                      }
                    >


                      {/* ========================================
                          RANK
                      ======================================== */}

                      <div className="rank">

                        #{index + 1}

                      </div>


                      {/* ========================================
                          DOCUMENT CONTENT
                      ======================================== */}

                      <div className="recommendation-content">


                        <div className="document-header">


                          <div className="document-title-area">

                            <div className="document-icon">

                              {getIcon(
                                recommendation.document
                              )}

                            </div>


                            <div>

                              <h3>
                                {recommendation.document}
                              </h3>

                              <span className="category">

                                {recommendation.category}

                              </span>

                            </div>

                          </div>


                          {/* SCORE */}

                          <div
                            className={`score ${getScoreClass(
                              score
                            )}`}
                          >

                            {percentage}%

                            <small>
                              match
                            </small>

                          </div>


                        </div>


                        {/* ======================================
                            SCORE BAR
                        ====================================== */}

                        <div className="score-background">

                          <div
                            className="score-fill"
                            style={{
                              width:
                                `${percentage}%`
                            }}
                          />

                        </div>


                        {/* ======================================
                            AI REASON
                        ====================================== */}

                        <div className="reason">

                          <span>
                            ✨
                          </span>

                          <div>

                            <strong>
                              Why this document?
                            </strong>

                            <p>
                              {recommendation.reason}
                            </p>

                          </div>

                        </div>


                        {/* ======================================
                            AI COMPONENT SCORES
                        ====================================== */}

                        <div className="ai-details">


                          <div className="ai-detail">

                            <span>
                              XGBoost
                            </span>

                            <strong>
                              {
                                formatScore(
                                  recommendation.xgb_score
                                )
                              }%
                            </strong>

                          </div>


                          <div className="ai-detail">

                            <span>
                              Semantic
                            </span>

                            <strong>
                              {
                                formatScore(
                                  recommendation.semantic_score
                                )
                              }%
                            </strong>

                          </div>


                          <div className="ai-detail">

                            <span>
                              Graph
                            </span>

                            <strong>
                              {
                                formatScore(
                                  recommendation.graph_score
                                )
                              }%
                            </strong>

                          </div>


                          <div className="ai-detail">

                            <span>
                              Business
                            </span>

                            <strong>
                              {
                                formatScore(
                                  recommendation.business_score
                                )
                              }%
                            </strong>

                          </div>


                        </div>


                      </div>

                    </div>

                  );

                }

              )}

            </div>


          </section>

        )}


      </main>


      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        <div>

          <strong>
            DigiLocker AI
          </strong>

          <span>
            Intelligent Document Recommendation System
          </span>

        </div>

        <span className="footer-tech">

          Powered by FastAPI + XGBoost + Semantic Search

        </span>

      </footer>


    </div>

  );
}


export default App;