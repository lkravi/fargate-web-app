#!/bin/bash
IP=$(curl -s http://checkip.amazonaws.com)
echo "{\"ip\": \"$IP\"}"
