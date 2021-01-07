from codecs import encode
import matplotlib
import matplotlib.pyplot as plt


def act_to_list(act_file):
    with open(act_file, 'rb') as act:
        raw_data = act.read()                           # Read binary data
    # Convert it to hexadecimal values
    hex_data = encode(raw_data, 'hex')
    # Get last 3 digits to get number of colors total
    total_colors_count = (int(hex_data[-7:-4], 16))
    # I have no idea what does it do
    misterious_count = (int(hex_data[-4:-3], 16))
    # Get last 3 digits to get number of nontransparent colors
    colors_count = (int(hex_data[-3:], 16))

    # Decode colors from hex to string and split it by 6
    # (because colors are #1c1c1c)
    colors = [hex_data[i:i + 6].decode()
              for i in range(0, total_colors_count * 6, 6)]

    # Add # to each item and filter empty items if there is a
    # corrupted total_colors_count bit
    colors = ['#' + i for i in colors if len(i)]

    return colors, total_colors_count


a, b = act_to_list('colourTable16.act')
print(a)

fig = plt.figure(figsize=(8, 0.5))
ax = fig.add_subplot(111)
patches = [matplotlib.patches.Rectangle(
    (100 * i, 0), 90, 90, color=c) for i, c in enumerate(a)]
for p in patches:
    ax.add_patch(p)

ax.axis("off")
plt.ylim(0, 90)
plt.xlim(0, 100 * len(a))
plt.show()
fig.savefig('colourtable.pdf', bbox_inches='tight')
