function onOpen() {
  DocumentApp.getUi()
    .createAddonMenu()
    .addItem("Activate Writing assistant", "showSidebar")
    .addToUi();
  showSidebar();
}

function showSidebar() {
  const htmlOutput = HtmlService.createHtmlOutputFromFile("FloatingIconSidebar")
    .setTitle("SynAI")
    .setWidth(400);
  DocumentApp.getUi().showSidebar(htmlOutput);
}

function performAction() {
  DocumentApp.getUi().alert("Icon clicked! Customize this action.");
}

function saveSystemPrompt(prompt) {
  Logger.log("System prompt saved: " + prompt);
  PropertiesService.getUserProperties().setProperty("systemPrompt", prompt);
}

function getSelectedText() {
  const selection = DocumentApp.getActiveDocument().getSelection();
  if (selection) {
    const elements = selection.getRangeElements();
    return elements.map((el) => el.getElement().asText().getText()).join("\n");
  }
  return "";
}

function getSuggestionsFromAPI(selectedText, systemPrompt) {
  const apiUrl = "https://writing-assistant-b13q.onrender.com/suggestions";

  const payload = {
    text: selectedText,
    prompt:
      systemPrompt ||
      "You are an experienced writer and linguist, you take in a sentence or a word, and provide a better reformulation. Make your response organized and clear to the user.",
  };

  const options = {
    method: "POST",
    contentType: "application/json",
    payload: JSON.stringify(payload),
  };

  try {
    const response = UrlFetchApp.fetch(apiUrl, options);
    const responseJson = JSON.parse(response.getContentText());

    // Return the suggestion from the API
    if (responseJson.suggestion) {
      return responseJson.suggestion;
    } else {
      throw new Error("No suggestion received");
    }
  } catch (error) {
    return `Error: ${error.message}`;
  }
}
