#!/usr/bin/env bash
set -euo pipefail

KEYSTORE_FILE="$(mktemp)"
trap 'rm -f "$KEYSTORE_FILE"' EXIT

echo "Decoding keystore to temporary file $KEYSTORE_FILE"
echo "$KEYSTORE" | base64 --decode > "$KEYSTORE_FILE"

echo "Signing bundle.zip with keystore $KEYSTORE_FILE"
jarsigner \
	-keystore "$KEYSTORE_FILE" \
	-storepass "$KEYSTORE_PASSWORD" \
	-keypass "$KEY_PASSWORD" \
	bundle.zip \
	"$KEY_ALIAS"
