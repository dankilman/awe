import awe

colors = ['#b47eb3', '#fdf5bf', '#ffd5ff', '#92d1c3', '#8bb8a8']
color = lambda i: colors[i % len(colors)]


def main():
    page = awe.Page()
    grid = page.new_grid(columns=3)
    for i in range(9):
        div = grid.new('div', style={
            'height': '240px',
            'textAlign': 'center',
            'backgroundColor': color(i)
        })
        lines = div.new_grid(columns=1)
        for _ in range(2):
            lines.new('br')
        lines.new('h1').new_text('Text')
        lines.new_text(str(i+1), style={
            'fontSize': '50px',
            'color': color(i+2)
        })
    page.start(block=True)


if __name__ == '__main__':
    main()
