import automat

s = automat.Automat("127.0.0.1", 8080)
p = s.Project("build-automat")
p.Build()
