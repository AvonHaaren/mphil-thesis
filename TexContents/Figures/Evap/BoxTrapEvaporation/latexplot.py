def latexplot(filename, keeppgf=False, keeptex=False, silent=True):
    import os
    import subprocess

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

    main = r'\input{' + filename + '.pgf}'

    content = header + main + footer

    with open(filename + '.tex', 'w') as f:
        f.write(content)

    commandLine = subprocess.Popen([
        'pdflatex',
        '--interaction=batchmode',
        filename + '.tex',
        '>', '/dev/null'
    ]) if silent else subprocess.Popen([
        'pdflatex',
        filename + '.tex'
    ])
    commandLine.communicate()
    if keeppgf is False:
        os.unlink(filename + '.pgf')
    if keeptex is False:
        os.unlink(filename + '.tex')
    os.unlink(filename + '.aux')
    # os.unlink(filename+'.log')

    commandLine = subprocess.Popen(['open', filename + '.pdf'])
    commandLine.communicate()

    return
