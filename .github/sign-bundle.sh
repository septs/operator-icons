#!/usr/bin/env bash
set -euo pipefail

KEYSTORE_FILE="$(mktemp)"
OPTS=(
	-keystore "$KEYSTORE_FILE"
	-storepass "$KEYSTORE_PASSWORD"
	-keypass "$KEY_PASSWORD"
	-tsa http://timestamp.digicert.com
)

cleanup() {
	rm --verbose --force "$KEYSTORE_FILE"
}

trap cleanup EXIT

echo "Decoding keystore to temporary file $KEYSTORE_FILE"
echo "$KEYSTORE" | base64 --decode >"$KEYSTORE_FILE"

echo "Signing bundle.zip with keystore $KEYSTORE_FILE"
jarsigner "${OPTS[@]}" bundle.zip "$KEY_ALIAS"

echo "Verifying signed bundle.zip"
jarsigner "${OPTS[@]}" -verify -verbose -certs bundle.zip >bundle.log
