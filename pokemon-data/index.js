var express = require("express"),
  bodyParser = require("body-parser"),
  smogon = require("@smogon/calc"),
  app = express(),
  port = process.env.PORT || 2001;

const { Pokemon } = require("@smogon/calc/dist/pokemon"),
  gen = smogon.Generations.get(7);
var attacker, defender, move, field, result, checkMove;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(bodyParser.raw());

// Get Routes
app.get("/", (req, res) => {
  return res.send("Nothing here...");
});

app.get("/calc", (req, res) => {
  return res.send(result);
});

app.get("/check-move", (req, res) => {
  return res.send(checkMove);
});

app.get("/pokemon-attacker", (req, res) => {
  return res.send(attacker);
});

app.get("/pokemon-defender", (req, res) => {
  return res.send(defender);
});

app.get("/attacking-move", (req, res) => {
  return res.send(move);
});

// Post Routes
app.post("/calc", (req, res) => {
  console.log("\n")
  result = smogon.calculate(gen, attacker, defender, move, field);
  res.sendStatus(200);
});

app.post("/check-move", (req, res) => {
  data = req.body;
  console.log("Got Move for Checking: " + data.name);
  checkMove = new smogon.Move(gen, data.name);
  res.sendStatus(200);
});

app.post("/pokemon-attacker", (req, res) => {
  data = req.body;
  console.log("Got Attacking Pokemon: " + data.name);
  attacker = new smogon.Pokemon(gen, data.name, {
    item: data.item,
    nature: data.nature,
    evs: {
      hp: data.evs[0],
      atk: data.evs[1],
      def: data.evs[2],
      spa: data.evs[3],
      spd: data.evs[4],
      spe: data.evs[5],
    },
    boosts: data.boosts,
  });
  res.sendStatus(200);
});

app.post("/pokemon-defender", (req, res) => {
  data = req.body;
  console.log("Got Defending Pokemon: " + data.name);
  defender = new smogon.Pokemon(gen, data.name, {
    item: data.item,
    nature: data.nature,
    evs: {
      hp: data.evs[0],
      atk: data.evs[1],
      def: data.evs[2],
      spa: data.evs[3],
      spd: data.evs[4],
      spe: data.evs[5],
    },
    boosts: data.boosts,
  });
  res.sendStatus(200);
});

app.post("/attacking-move", (req, res) => {
  data = req.body;
  console.log("Got Move: " + data.name);
  move = new smogon.Move(gen, data.name);
  res.sendStatus(200);
});

app.listen(port, () => {
  console.log("Server started on port: " + port);
});

/*
import pkg from '@smogon/calc';

const gen = pkg.Generations.get(6)
const result = pkg.calculate(
    gen,
    new pkg.Pokemon(gen, 'Gengar', {
      item: 'Choice Specs',
      nature: 'Timid',
      evs: {spa: 252},
      boosts: {spa: 1},
    }),
    new pkg.Pokemon(gen, 'Chansey', {
      item: 'Eviolite',
      nature: 'Calm',
      evs: {hp: 252, spd: 252},
    }),
    new pkg.Move(gen, 'Focus Blast')
  );

  console.log(result)
  */
