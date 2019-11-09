const express = require('express')
const jwt = require('jsonwebtoken')
const cors = require('cors')
const bodyparser = require('body-parser')
const expressjwt = require('express-jwt')

const mongo = require('mongodb').MongoClient
const murl = 'mongodb://localhost:27017'
const dbname = 'test_bot_database'
const client = new mongo(murl)
var db = null
client.connect((err) => {
    db = client.db(dbname)
})

const adminUser = {username:"admin",password:"admin"}
const JWT_secret = "cobot_api_123098"
app = express()
app.use(cors())
app.use(bodyparser.json())
//app.use(expressjwt({secret:JWT_secret}).unless({path:['/api/auth']}))

app.post('/api/auth',(req,res) => {
    if(req.body) {
        user = req.body.user
        if(adminUser.username==user.username && adminUser.password==user.password) {
            token = jwt.sign(user,JWT_secret)
            res.status(200).send({user: adminUser.username,token: token})
        } else {
            res.status(403).send({errorMessage: "Wrong username/password"})    
        }

    } else {
        res.status(403).send({errorMessage: "No username"})
    }
})

app.get('/api/locations', async (req,res) => {
    if(db==null) {
        res.send({error: "No database"})
        return
    }
    const locs = db.collection('locations')
    const docs = await locs.find().toArray()
    res.status(200).send(docs)
})

app.post('/api/locations', async (req,res) => {
    try {
        if(db==null) {
            res.send({error: "No database"})
            return
        }
        const locs = db.collection('locations')
        const r = await locs.insertOne(req.body.location)
        res.status(200).send({insert: r.insertedCount,id:r.insertedId})
    } catch(err) {
        res.status(500).send(err)
    }
})

app.delete('/api/locations', async (req,res) => {
    try {
        if(db==null) {
            res.send({error: "No database"})
            return
        }
        console.log(req.body)
        const r = await db.collection('locations').deleteOne({_id:req.body.location._id})
        res.status(200).send({deleted:r.deletedCount})
    } catch(err) {
        res.status(500).send(err)
    }
})



app.get('/api/users', async (req,res) => {
    try {
        if(db==null) {
            res.send({error: "No database"})
            return
        }
        const users = db.collection('users')
        const docs = await users.find().toArray()
        res.status(200).send(docs)
            
    } catch (error) {
        res.status(500).send(err)
    }
})

app.delete('/api/users', async (req,res) => {
    try {
        if(db==null) {
            res.send({error: "No database"})
            return
        }
        const r = await db.collection('users').deleteOne({_id:req.body.user._id})
        res.status(200).send({deleted:r.deletedCount})
            
    } catch (error) {
        res.status(500).send(err)        
    }
})



app.listen(8080,()=>console.log("started at 8080"))
