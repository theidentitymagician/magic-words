// Paste into javascript_tool on the LIVE Systeme page (not the editor).
// Lists every element ID inside the page with its size, so you can swap IDs in checkout_header_code.css.
[...document.querySelectorAll('section [id]')]
  .filter(e => !/^(card|stripe)/i.test(e.id))
  .map(e => { const r = e.getBoundingClientRect(); let d = 0, p = e; while (p && p.tagName !== 'SECTION') { p = p.parentElement; d++; }
    return d + ' ' + e.tagName + '#' + e.id + ' y' + Math.round(r.top + scrollY) + ' h' + Math.round(r.height) + ' w' + Math.round(r.width) + ' ' + (e.innerText || '').slice(0, 30).replace(/\n/g, ' '); })
  .join('\n')
