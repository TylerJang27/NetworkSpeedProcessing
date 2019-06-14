  $reading = fopen('D:\Documents D\DUKEDEVILS\Code+\PracticeCoding\data.txt', 'r');
  $writing = fopen('D:\Documents D\DUKEDEVILS\Code+\PracticeCoding\data.txt.tmp', 'w');

  $replaced = false;

  while (!feof($reading)) {
    $line = fgets($reading);
    if (stristr($line,'word')) {
      $line = "word=\"new word\"\n";
      $replaced = true;
    }
    fputs($writing, $line);
  }
  fclose($reading); fclose($writing);
  // might as well not overwrite the file if we didn't replace anything
  if ($replaced)
  {
    rename('D:\Documents D\DUKEDEVILS\Code+\PracticeCoding\data.txt.tmp', 'D:\Documents D\DUKEDEVILS\Code+\PracticeCoding\data.txt');
  } else {
    unlink('D:\Documents D\DUKEDEVILS\Code+\PracticeCoding\data.txt');
  }
