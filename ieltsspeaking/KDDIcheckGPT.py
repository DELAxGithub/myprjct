// OpenAIのAPIキーを設定します。
var openai_api_key = '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';

function rewrite_text(original_text) {
    var url = 'https://api.openai.com/v1/engines/davinci-codex/completions';
    var options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + openai_api_key
        },
        payload: JSON.stringify({
            'prompt': original_text + '\n\nRewrite this text:',
            'max_tokens': 60
        })
    };
    var response = UrlFetchApp.fetch(url, options);
    var data = JSON.parse(response.getContentText());
    return data['choices'][0]['text'];
}

function correct_sheet() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('Sheet1');  // ここにあなたのシートの名前を入れてください。
    var range = sheet.getRange('A1:A' + sheet.getLastRow());
    var values = range.getValues();

    for (var i = 0; i < values.length; i++) {
        var original_text = values[i][0];
        var rewritten_text = rewrite_text(original_text);
        sheet.getRange('B' + (i + 1)).setValue(rewritten_text);
    }
}
