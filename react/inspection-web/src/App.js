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
          <div className="tab-content">
            <h2>Home</h2>
            <p>소화기 점검 시스템 메인 화면</p>
            <div className="home-card-grid">
              <div className="home-card">총 소화기 : 3대</div>
              <div className="home-card">정상 : 2대</div>
              <div className="home-card">불량 : 1대</div>
            </div>
          </div>
        );

      case "id1":
        return (
          <div className="tab-content">
            <h2>ID : 1</h2>
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
            <h2>ID : 2</h2>
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
            <h2>ID : 3</h2>
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
