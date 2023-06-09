import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileObject, setSelectedFileObject] = useState(null);
  const [predictedRoaster, setPredictedRoaster] = useState(null);
  const [actualRoaster, setActualRoaster] = useState('');
  const [lastEnteredRoaster, setLastEnteredRoaster] = useState(''); // New state variable
  const [actualBean, setActualBean] = useState('');
  const [lastEnteredBean, setLastEnteredBean] = useState('');
  const [predictionCorrect, setPredictionCorrect] = useState(null);
  const [showResetButton, setShowResetButton] = useState(false);
  const [roasterInfo, setRoasterInfo] = useState(null);
  const fileInputRef = useRef(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  const fileSelectedHandler = async (event) => {
    if (event.target.files.length === 0) {
      return;
    }
    setSelectedFile(URL.createObjectURL(event.target.files[0]));
    setSelectedFileObject(event.target.files[0]);

    const formData = new FormData();
    formData.append('file', event.target.files[0]);

    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setPredictedRoaster(data.prediction);
    setRoasterInfo(data.roaster_info);
    setShowResetButton(true);
  };

  const chooseFileHandler = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.capture = 'environment';
    input.onchange = fileSelectedHandler;
    input.click();
  };

  const resetPage = () => {
    setSelectedFile(null);
    setSelectedFileObject(null);
    setPredictedRoaster(null);
    setActualRoaster('');
    setActualBean('');
    setPredictionCorrect(null);
    setShowResetButton(false);
    setRoasterInfo(null);
  };

  const submitFeedback = async () => {
    let formData = new FormData();
    formData.append('file', selectedFileObject);
    formData.append('predicted_roaster', predictedRoaster);
    formData.append('actual_roaster', actualRoaster);
    formData.append('actual_bean', actualBean);
    formData.append('prediction_correct', predictionCorrect);
    setShowResetButton(false);

    const response = await fetch('http://localhost:5000/feedback', {
      method: 'POST',
      body: formData,
    });

    
    if (response.ok) {
      setFeedbackSubmitted(true);
      setLastEnteredRoaster(actualRoaster); // Store the last entered roaster
      setLastEnteredBean(actualBean); // Store the last entered bean
      setSelectedFile(null);
      setPredictedRoaster(null);
      setActualRoaster('');
      setActualBean('');
      setPredictionCorrect(null);
      setTimeout(() => {
        setFeedbackSubmitted(false);
      }, 3000);
    } else {
      alert('Something went wrong. Please try again.');
    }
  };

  const handleYesButtonClick = () => {
    setPredictionCorrect(true);
  };

  const handleNoButtonClick = () => {
    setPredictionCorrect(false);
  };

  const useLastRoaster = () => {
    setActualRoaster(lastEnteredRoaster); // Set the actual roaster value as the last entered roaster
  };

  const useLastBean = () => {
    setActualBean(lastEnteredBean); // Set the actual bean value as the last entered bean
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hi, I'm Latto, the craft coffee companion</h1>
        <p>Please upload an image of your coffee bag:</p>
        <label htmlFor="fileInput" className="fileInputLabel">
          Choose File
          <input
            id="fileInput"
            ref={fileInputRef}
            type="file"
            onChange={fileSelectedHandler}
            style={{ display: 'none' }}
          />
        </label>
        <button onClick={chooseFileHandler}>Take Picture</button>
        {selectedFile && <img src={selectedFile} alt="Coffee bag" height="200" />}
        {predictedRoaster && (
          <div>
            <p>The predicted roaster is: {predictedRoaster}</p>
            {roasterInfo && (
              <div className="roaster-table">
                <table>
                  <thead>
                    <tr>
                      <th>Roaster</th>
                      <th>Bean</th>
                      <th>Price</th>
                      <th>Number of Reviews</th>
                      <th>Rating</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{roasterInfo.roaster}</td>
                      <td>{roasterInfo.bean}</td>
                      <td>{roasterInfo.price && roasterInfo.price.replace(/[^\d.]/g, '')}</td>
                      <td>{roasterInfo.number_of_reviews}</td>
                      <td>{roasterInfo.rating}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            )}
            <p>Is this correct?</p>
            <button onClick={handleYesButtonClick}>Yes</button>
            <button onClick={handleNoButtonClick}>No</button>
            {predictionCorrect !== null && (
              <div>
                {predictionCorrect ? (
                  <input
                    type="text"
                    placeholder="Actual bean"
                    value={actualBean}
                    onChange={(e) => setActualBean(e.target.value)}
                  />
                ) : (
                  <div>
                    <input
                      type="text"
                      placeholder="Actual roaster"
                      value={actualRoaster}
                      onChange={(e) => setActualRoaster(e.target.value)}
                    />
                    <input
                      type="text"
                      placeholder="Actual bean"
                      value={actualBean}
                      onChange={(e) => setActualBean(e.target.value)}
                    />
                  </div>
                )}
                <button onClick={submitFeedback}>Submit feedback</button>
                {lastEnteredRoaster && (
                  <button onClick={useLastRoaster}>Use Last Roaster</button>
                )}
                {lastEnteredBean && (
                  <button onClick={useLastBean}>Use Last Bean</button>
                )}
              </div>
            )}
          </div>
        )}
        {showResetButton && <button onClick={resetPage}>Reset</button>}
        {feedbackSubmitted && (
          <div>
            <p>Feedback submitted. Thank you!</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;