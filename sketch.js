// PARAMS will be embedded here

function setup() {
    createCanvas(WIDTH, HEIGHT);
    stroke('black');
    fill(CIRCLE_COLOR);
}

function draw() {
    background(BACKGROUND_COLOR);
    circle(mouseX, mouseY, CIRCLE_SIZE);
}

function mouseClicked() {
    // coordinates are passed to Streamlit
    let values = {
        x: mouseX,
        y: mouseY
    }
    window.parent.stBridges.send('my-bridge', values);
}