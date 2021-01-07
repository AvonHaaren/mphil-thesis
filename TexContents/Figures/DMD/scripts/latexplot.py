def latexplot(filepath, keeppgf=False, keeptex=False, silent=True):
    import os
    import subprocess
    import platform
    from pathlib import Path

    cwd = os.getcwd()
    os.chdir(filepath.parent)

    filename = filepath.name

    header = r'''\documentclass[11pt]{standalone}
    \usepackage[utf8]{inputenc}
    \DeclareUnicodeCharacter{2212}{$-$}
    \usepackage[UKenglish]{babel}
    \usepackage{amsmath}
    \usepackage{amsfonts}
    \usepackage{amssymb}
    \usepackage{gensymb}
    \usepackage{graphicx}
    \usepackage{siunitx}
    \sisetup{locale = UK,
        per-mode = fraction}
    \usepackage{pgfplots}
    \pgfplotsset{compat=1.16}
    \begin{document}
    '''

    footer = r'''
    \end{document}'''

    main = r'\input{' + filename + r'}'

    content = header + main + footer

    texName = filepath.stem + '.tex'
    with open(texName, 'w') as f:
        f.write(content)

    commandLine = subprocess.Popen([
        'pdflatex',
        '--interaction=batchmode',
        texName,
        '>', '/dev/null'
    ], stdout=subprocess.PIPE) if silent else subprocess.Popen([
        'pdflatex',
        texName
    ], stdout=subprocess.PIPE)
    data = commandLine.communicate()[0]
    RC = commandLine.returncode

    if keeptex is False:
        os.unlink(texName)
    os.unlink(filepath.stem + '.aux')
    if RC == 0:
        if keeppgf is False:
            os.unlink(filename)
        os.unlink(filepath.stem + '.log')
    else:
        subprocess.run(['code', '-n', filepath.stem + '.log'])
        return

    if platform.system() != "Windows":
        subprocess.run(
            ['open', filepath.stem + '.pdf'])

    os.chdir(cwd)
    return
