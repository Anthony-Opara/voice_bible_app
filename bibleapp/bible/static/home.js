$(document).ready(function() {
    var jsonObj = [];
    var queueList = [];
  
    $.getJSON(
      "https://raw.githubusercontent.com/jplehmann/textbites/master/textbites/data/NKJV.bible.json",
      function(json) {
        // point jsonObj to the .json file.
        jsonObj = json;
  
        //Populate booklist
        jsonObj.books.forEach(function(val, i) {
          var option = new Option(val.name, i, false, false);
          $("#book-selector").append(option);
        });
  
        PopulateChapterList(0);
  
        PopulateVerseList(0, 0);
      }
    );
  
    function PopulateChapterList(bookindex) {
      // Clear Chapter List first
      document.getElementById("chapter-selector").innerHTML = "";
      // Populate list
      jsonObj.books[bookindex].chapters.forEach(function(val, i) {
        var option = new Option(i + 1, i, false, false);
        $("#chapter-selector").append(option);
      });
    }
  
    function PopulateVerseList(bookindex, chapterindex) {
      // Clear Verse List first
      document.getElementById("verse-selector").innerHTML = "";
      // Populate list
      jsonObj.books[bookindex].chapters[chapterindex].verses.forEach(function(
        val,
        i
      ) {
        var option = new Option(val.num, i, false, false);
        $("#verse-selector").append(option);
      });
    }
  
    function GetBookSelectedIndex() {
      // get booklist element
      var blist = document.getElementById("book-selector");
      // get current selected book index from option value
      return blist.options[blist.selectedIndex].value;
    }
  
    function GetBookName() {
      // get booklist element
      var blist = document.getElementById("book-selector");
      // get current selected book index from option value
      return blist.options[blist.selectedIndex].text;
    }
  
    function GetChapterSelectedIndex() {
      // get chapterlist element
      var clist = document.getElementById("chapter-selector");
      // get current selected chapter index from option value
      return clist.options[clist.selectedIndex].value;
    }
  
    function GetChapterNumber() {
      // get chapterlist element
      var clist = document.getElementById("chapter-selector");
      // get current selected chapter index from option value
      return clist.options[clist.selectedIndex].text;
    }
  
    function GetVerseSelectedIndex() {
      // get verselist element
      var vlist = document.getElementById("verse-selector");
      // get current selected verse index from option value
      return vlist.options[vlist.selectedIndex].value;
    }
  
    function GetVerseNumber() {
      // get verselist element
      var vlist = document.getElementById("verse-selector");
      // get current selected verse index from option value
      return vlist.options[vlist.selectedIndex].text;
    }
  
    function GetVerseText(bookindex, chapterindex, verseindex) {
      return jsonObj
        .books[bookindex].chapters[chapterindex].verses[verseindex].text;
    }
  
    // On booklist change,
    // populate the chapter list for
    // the current selected book
    $("#book-selector").on("change", function() {
      // populate chapter list with chapters for selected book
      PopulateChapterList(GetBookSelectedIndex());
      // populate verse list for chapter 1
      PopulateVerseList(GetBookSelectedIndex(), 0);
    });
  
    // On chapterlist change,
    // populate the verse list for
    // the current selected chapter
    $("#chapter-selector").on("change", function() {
      // populate verse list for chapter 1
      PopulateVerseList(GetBookSelectedIndex(), GetChapterSelectedIndex());
    });})