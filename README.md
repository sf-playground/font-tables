# font-tables

> An OpenType font table reporting tool for ttf and otf files

## Usage

```
python font-tables.py [fontpath 1] [fontpath 2] [fontpath n...]
```

The report is available on the path `otreports/[fontpath]-TABLES.yaml` after you execute the above command.  The file write takes place on a path relative to the directory that contains the `font-tables.py` script.

The success of table reporting is indicated in the standard output stream.  Indicators include:

- `[✓]` = successful write of the table contents to the report file
- `[E]` = empty table, the table is not included in the report file
