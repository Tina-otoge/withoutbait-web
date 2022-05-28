for (let el of document.querySelectorAll("[data-date-fmt]")) {
  let date = luxon.DateTime.fromISO(el.innerHTML.replace(" ", "T"), {zone: 'utc'});
  el.setAttribute("title", date.toLocal().toLocaleString(luxon.DateTime.DATETIME_FULL));
  el.innerHTML = date.toRelative();
}
