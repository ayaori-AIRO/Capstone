import { useEffect, useState } from "react";
import { collection, getDocs, query, orderBy } from "firebase/firestore";
import { db } from "./firebase";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [activeTab, setActiveTab] = useState("home");

  useEffect(() => {
    const loadData = async () => {
      const q = query(
        collection(db, "inspection"),
        orderBy("time", "desc")
      );

      const querySnapshot = await getDocs(q);

      const result = querySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      setData(result);
    };

    loadData();
  }, []);

  const renderTabContent = () => {
    switch (activeTab) {
      case "home":
  return (
    <div
      className="tab-content"
      style={{
        display: "flex",
        gap: "10px",
        height: "100%",
        alignItems: "stretch"
      }}
    >
      {/* 🔵 왼쪽 카드 */}
      <div
        className="home-card-grid"
        style={{ alignSelf: "flex-start" }}
      >
        <div className="home-card">총 소화기 : 3대</div>
        <div className="home-card">정상 : 2대</div>
        <div className="home-card">불량 : 1대</div>
      </div>

      {/* 🟢 가운데 여백 */}
      <div style={{ flex: 1 }} />

      {/* 🔴 오른쪽 전체 영역 */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          width: "140px",
          height: "100%",
          justifyContent: "space-between"
        }}
      >
        {/* ───── 위: 개별 검사 박스 ───── */}
        <div>
          {/* 제목 */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              borderTop: "2px solid #444",
              borderLeft: "2px solid #444",
              borderRight: "2px solid #444",
              padding: "4px 8px",
              borderTopLeftRadius: "8px",
              borderTopRightRadius: "8px",
              fontWeight: 600
            }}
          >
            개별 검사
          </div>

          {/* 버튼 영역 */}
          <div
            style={{
              borderLeft: "2px solid #444",
              borderRight: "2px solid #444",
              borderBottom: "2px solid #444",
              borderBottomLeftRadius: "8px",
              borderBottomRightRadius: "8px",
              display: "flex",
              flexDirection: "column",
              gap: "10px",
              padding: "12px"
            }}
          >
            <button>ID : 1</button>
            <button>ID : 2</button>
            <button>ID : 3</button>

            {/* 구분선 */}
            <div
              style={{
                height: "1px",
                background: "#444",
                margin: "6px 0"
              }}
            />

            {/* ───── 아래: 검사 복귀 영역 ───── */}
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <div
                style={{
                  textAlign: "center",
                  fontWeight: 600
                }}
              >
                검사 · 복귀
              </div>

              {/* 🔵 추가 버튼 2개 */}
              <div style={{ marginTop: "10px", display: "flex", flexDirection: "column", gap: "8px" }}>
                <button
                  style={{
                    backgroundColor: "#007bff",
                    color: "#fff",
                    padding: "6px",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  홈 위치
                </button>

                <button
                  style={{
                    backgroundColor: "#28a745",
                    color: "#fff",
                    padding: "6px",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  검사 실행
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

      case "id1":
        return (
          <div className="tab-content">
            <p>1번 소화기 상세 정보</p>
            <div className="detail-box">
              <div>위치 : B1F 복도 A</div>
              <div>압력 : 정상</div>
              <div>외관 : 양호</div>
              <div>결과 : 합격</div>
            </div>
          </div>
        );

      case "id2":
        return (
          <div className="tab-content">
            <p>2번 소화기 상세 정보</p>
            <div className="detail-box">
              <div>위치 : B1F 복도 B</div>
              <div>압력 : 낮음</div>
              <div>외관 : 양호</div>
              <div>결과 : 불합격</div>
            </div>
          </div>
        );

      case "id3":
        return (
          <div className="tab-content">
            <p>3번 소화기 상세 정보</p>
            <div className="detail-box">
              <div>위치 : B1F 비상구 앞</div>
              <div>압력 : 정상</div>
              <div>외관 : 오염</div>
              <div>결과 : 불합격</div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="container">
      <h1> 🧯 소화기 점검 시스템 🧯</h1>

      <div className="content-row">
        <div className="map-section">
          <h2>B1F 맵</h2>
          <img src="/B1F.jpg" alt="B1F Map" className="map-image" />
        </div>

        <div className="right-section">
          <div className="extra-section">
            <div className="tab-header">
              <button
                className={`tab-button ${activeTab === "home" ? "active" : ""}`}
                onClick={() => setActiveTab("home")}
              >
                Home
              </button>

              <button
                className={`tab-button ${activeTab === "id1" ? "active" : ""}`}
                onClick={() => setActiveTab("id1")}
              >
                ID : 1
              </button>

              <button
                className={`tab-button ${activeTab === "id2" ? "active" : ""}`}
                onClick={() => setActiveTab("id2")}
              >
                ID : 2
              </button>

              <button
                className={`tab-button ${activeTab === "id3" ? "active" : ""}`}
                onClick={() => setActiveTab("id3")}
              >
                ID : 3
              </button>
            </div>

            <div className="tab-body">{renderTabContent()}</div>
          </div>

          <div className="table-section">
            <h2>검사 결과</h2>

            <table className="inspection-table">
              <thead>
                <tr>
                  <th>No</th>
                  <th>소화기 ID</th>
                  <th>위치</th>
                  <th>압력</th>
                  <th>외관</th>
                  <th>결과</th>
                  <th>시간</th>
                </tr>
              </thead>

              <tbody>
                {data.map((item, index) => (
                  <tr key={item.id}>
                    <td>{index + 1}</td>
                    <td>{item.extinguisher_id}</td>
                    <td>{item.location}</td>
                    <td>{item.pressure === "normal" ? "정상" : "낮음"}</td>
                    <td>{item.appearance === "clean" ? "양호" : "오염"}</td>
                    <td
                      className={
                        item.result === "pass"
                          ? "result-pass"
                          : "result-fail"
                      }
                    >
                      {item.result === "pass" ? "합격" : "불합격"}
                    </td>
                    <td>{item.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
