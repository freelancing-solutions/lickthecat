import time
from flask import Flask, render_template, request, Blueprint
import solana
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import transfer
from solana.publickey import PublicKey
from solana.keypair import Keypair

from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

# Flask Blueprint
lick_blueprint = Blueprint('lick', __name__, template_folder='templates')

# Configurations
RPC_URL = "https://api.mainnet-beta.solana.com"  # Use a valid Solana RPC
client = Client(RPC_URL)

# Default Values (Can be updated from Dashboard)
config = {
    "pump_fun_contract": "PumpFunContractAddress",
    "buyer_wallet_secret": "YOUR_SECRET_KEY",
    "token_vault": "YourVaultAddress",
    "batch_size": 10,
    "total_budget": 120,
    "delay": 5
}


def get_lick_balance():
    token = Token(client, PublicKey(config["token_vault"]), TOKEN_PROGRAM_ID, get_wallet())
    token_balance = token.get_balance(get_wallet().public_key)
    return token_balance['result']['value'] / 1e9  # Convert from lamports to tokens

def get_wallet():
    return Keypair.from_secret_key(bytes.fromhex(config["buyer_wallet_secret"]))

def get_balance():
    return client.get_balance(get_wallet().public_key)["result"]["value"] / 1e9

def buy_tokens(amount_sol):
    tx = Transaction()
    tx.add(transfer(
        solana.system_program.TransferParams(
            from_pubkey=get_wallet().public_key,
            to_pubkey=PublicKey(config["pump_fun_contract"]),
            lamports=int(amount_sol * 1e9)  # Convert SOL to lamports
        )
    ))
    response = client.send_transaction(tx, get_wallet())
    return response

@lick_blueprint.route('/')
def index():
    sol_balance = get_balance()
    lick_balance = get_lick_balance()
    return render_template('dashboard.html', sol_balance=sol_balance, lick_balance=lick_balance, config=config)

@lick_blueprint.route('/')
def index():
    return render_template('dashboard.html', config=config)

@lick_blueprint.route('/update_config', methods=['POST'])
def update_config():
    global config
    config["pump_fun_contract"] = request.form["pump_fun_contract"]
    config["buyer_wallet_secret"] = request.form["buyer_wallet_secret"]
    config["token_vault"] = request.form["token_vault"]
    config["batch_size"] = int(request.form["batch_size"])
    config["total_budget"] = int(request.form["total_budget"])
    config["delay"] = int(request.form["delay"])
    return {"message": "Configuration updated successfully", "config": config}

@lick_blueprint.route('/start', methods=['POST'])
def start_buying():
    global config
    sol_left = config["total_budget"]
    while sol_left > 0:
        batch_amount = min(config["batch_size"], sol_left)
        response = buy_tokens(batch_amount)
        sol_left -= batch_amount
        time.sleep(config["delay"])  # Wait before the next buy
    return {"message": "Finished purchasing LICK tokens", "sol_left": sol_left}

# Flask App Setup
app = Flask(__name__)
app.register_blueprint(lick_blueprint, url_prefix='/lick')

if __name__ == "__main__":
    app.run(debug=True)
