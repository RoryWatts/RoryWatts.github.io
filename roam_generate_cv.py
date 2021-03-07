import roam_cv

x = roam_cv.RoamZip()
y = x.cv
z = roam_cv.MarkdownExporter(y)
z.export_as_markdown()