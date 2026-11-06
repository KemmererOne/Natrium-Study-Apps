// Where feedback and error reports go. This address is public: anyone can read it in the site's code.
const FEEDBACK_EMAIL = "natriumfundamentals@gmail.com";

function mailto(subject, body) {
  return "mailto:" + FEEDBACK_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
}

// A report about one quiz question or flashcard. The ID says which item to fix;
// the rest lets the reader confirm it. Long text is cut to keep the link short.
function itemReport(id, topic, text, src) {
  const shown = text.length > 160 ? text.slice(0, 160) + "..." : text;
  return mailto("Problem with " + id, "Item: " + id + "\nTopic: " + topic + "\nQuestion: " + shown + "\nSource: " + src + "\n\nWhat looks wrong:\n");
}
