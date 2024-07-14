"""Linear regression example"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

import nada_numpy as na
import nada_numpy.client as na_client
import numpy as np
import py_nillion_client as nillion
from common.utils import compute, store_program, store_secrets
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from dotenv import load_dotenv
from nillion_python_helpers import (create_nillion_client,
                                    create_payments_config)
from py_nillion_client import (Integer, SecretInteger, SecretUnsignedInteger,
                               UnsignedInteger)
from py_nillion_client import NodeKey, UserKey
from sklearn.linear_model import LinearRegression

from nada_ai.client import SklearnClient
from transformers import BertModel, BertTokenizer
from nada_ai.nada_typing import NillionType
from abc import ABC, ABCMeta
from typing import Any, Dict, Sequence

import nada_numpy.client as na_client
import numpy as np
import torch
from random import random

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

NUM_FEATS = 10


# Main asynchronous function to coordinate the process
async def main() -> None:
    """Main nada program"""

    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

    seed = "my_seed_" + str(int((random()) * 10** 8))
    userkey = UserKey.from_seed((seed))
    nodekey = NodeKey.from_seed((seed))
    client = create_nillion_client(userkey, nodekey)
    party_id = client.party_id
    user_id = client.user_id

    party_names = na_client.parties(2)
    program_name = "linear_regression"
    program_mir_path = f"target/{program_name}.nada.bin"

    # Configure payments
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    # Store program
    program_id = await store_program(
        client,
        payments_wallet,
        payments_client,
        user_id,
        cluster_id,
        program_name,
        program_mir_path,
    )

    # # Train a linear regression
    # X = np.random.randn(1000, NUM_FEATS)
    # # We generate the data from a specific linear model
    # coeffs_gt = np.ones(
    #     NUM_FEATS,
    # )
    # bias_gt = 4.2

    # y = X @ coeffs_gt + bias_gt

    # model = LinearRegression()
    # # The learned params will likely be close to the coefficients & bias we used to generate the data
    # fit_model = model.fit(X, y)

    # print("Learned model coeffs are:", model.coef_)
    # print("Learned model intercept is:", model.intercept_)

    model_name = 'bert-base-uncased'
    model = BertModel.from_pretrained(model_name)
    # tokenizer = BertTokenizer.from_pretrained(model_name)

    def export_state_as_secrets(
        self,
        name: str,
        nada_type: NillionType,
    ) -> Dict[str, NillionType]:
        """
        Exports model state as a Dict of Nillion secret types.

        Args:
            name (str): Name to be used to store state secrets in the network.
            nada_type (NillionType): Data type to convert weights to.

        Raises:
            NotImplementedError: Raised when unsupported model state type is passed.
            TypeError: Raised when model state has incompatible values.

        Returns:
            Dict[str, NillionType]: Dict of Nillion secret types that represents model state.
        """
        state_secrets = {}
        for state_layer_name, state_layer_weight in self.state_dict.items():
            layer_name = f"{name}_{state_layer_name}"
            layer_state = self.__ensure_numpy(state_layer_weight)
            state_secret = na_client.array(layer_state, layer_name, nada_type)
            state_secrets.update(state_secret)

        return state_secrets

    # print(model.state_dict())

    # def add_param_bert(self):
    #     self.state_dict = 

    #         state_dict = {"coef": model.coef_}
    #         print(model.coef_)
    #         if model.fit_intercept is True:
    #             state_dict.update({"intercept": model.intercept_})
    #     else:
    #         error_msg = (
    #             f"Instantiating SklearnClient from `{type(model)}` is not implemented."
    #         )
    #         raise NotImplementedError(error_msg)

    #     self.state_dict = state_dict

    # Create and store model secrets via ModelClient
    model_client = model#{"coef": model.state_dict()}
    nada_type = nillion.SecretInteger
    
        # print(numpy_array)
        # dict_weights[name] = numpy_array
    i = 0
    for state_layer_name, state_layer_weight in model.state_dict().items():
        if i:
            print(1)
            state_secrets = {}
            print(2)
            layer_name = f"my_model_{state_layer_name}"
            print(3)
            # layer_state = model_client.__ensure_numpy(state_layer_weight)
            layer_state = state_layer_weight.detach().cpu().numpy()
            print(3.5)
            # print(layer_state)
            layer_state_secret = [[nillion.SecretInteger(int(i)) for i in layer] for layer in layer_state]
            print(4)
            # state_secret = {k: v for i in range(arr.shape[0]) for k, v in array(arr[i], f"{prefix}_{i}", nada_type).items()}
            # state_secret = na_client.array(layer_state, layer_name, nada_type)
            state_secret = {}

            for j in range(layer_state.shape[0]):
                for i in range(layer_state[j].shape[0]):
                    state_secret[layer_name + "_" + str(i) + "_weight_nbr_" + str(j)] = layer_state_secret[j][i]
            print(4.5)
            # state_secret = dict(zip([layer_name + "_" + str(i) + "_weight_nbr" + str(j)], layer_state_secret))
            # print(state_secret)
            # # for name, param in model.state_dict().items():
            #     # print(f"Layer: {name}, Shape: {param.shape}")
            #     # print(param)  # This will print the tensor values

            #     # If you want to convert the tensor to a numpy array
            #     numpy_array = param.detach().cpu().numpy()
            #     # print(numpy_array)
            #     dict_weights[name] = numpy_array

            # dict_secret_weight =
            print(5)
            state_secrets.update(state_secret)
            print(6)
            
            model_secrets = nillion.NadaValues(state_secrets)
            print(7)
            # print("state_secrets")
            # print(state_secrets)
            #     model_client.export_state_as_secrets("my_model", na.SecretRational)
            # )
            print(8)
            permissions = nillion.Permissions.default_for_user(client.user_id)
            print(9)
            permissions.add_compute_permissions({client.user_id: {program_id}})
            print(10)

            model_store_id = await store_secrets(
                client,
                payments_wallet,
                payments_client,
                cluster_id,
                model_secrets,
                1,
                permissions,
            )
            print(11)
            break
        else:
            i += 1
    print("stored 1")
        # state_secrets


    # # Store inputs to perform inference for
    # my_input = na_client.array(np.ones((NUM_FEATS,)), "my_input", na.SecretRational)
    # input_secrets = nillion.NadaValues(my_input)

    # data_store_id = await store_secrets(
    #     client,
    #     payments_wallet,
    #     payments_client,
    #     cluster_id,
    #     input_secrets,
    #     1,
    #     permissions,
    # )

    # Set up the compute bindings for the parties
    compute_bindings = nillion.ProgramBindings(program_id)

    for party_name in party_names:
        compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_names[-1], party_id)

    print(f"Computing using program {program_id}")
    # print(f"Use secret store_id: {model_store_id} {data_store_id}")
    print(f"Use secret store_id: {model_store_id}")

    # Create a computation time secret to use
    computation_time_secrets = nillion.NadaValues({})

    # Compute, passing all params including the receipt that shows proof of payment
    result = await compute(
        client,
        payments_wallet,
        payments_client,
        program_id,
        cluster_id,
        compute_bindings,
        # [model_store_id, data_store_id],
        [model_store_id],
        computation_time_secrets,
        verbose=True,
    )

    # # Rescale the obtained result by the quantization scale
    # outputs = [na_client.float_from_rational(result["my_output"])]
    # print(f"🖥️  The result is {outputs} @ {na.get_log_scale()}-bit precision")

    # expected = fit_model.predict(np.ones((NUM_FEATS,)).reshape(1, -1))
    # print(f"🖥️  VS expected result {expected}")


if __name__ == "__main__":
    asyncio.run(main())