# Reverse Analysis of Zhihu x-zse-96 Request Header Parameter

## Introduction
This document details the entire reverse analysis process of the `x-zse-96` parameter in Zhihu's request header, covering key links such as encryption location positioning, call stack debugging, Webpack loader parsing, and encryption algorithm identification.

## Reverse Steps

### 1. Preliminary Positioning of Encryption Location
Analyze the request header with the third-party tool `curlCoverter` to confirm that `x-zse-96` is an encrypted parameter, then locate the approximate encryption position of the parameter via the **XHR breakpoint** method:
- Enter content in the search box and press Enter to trigger the request. Observe that `x-zse-96` in the request header has been encrypted, so switch to call stack debugging.

### 2. Locate Core Function via Call Stack Debugging
- After debugging the call stack, locate that the core generation logic of `x-zse-96` encryption is dominated by the `ej` function. Focus on the value of the `eL` variable and enter the `eb` function.
- Find that `eh` and `ep` adopt the Webpack loader module packaging method, and further analysis is required for the characteristics of Webpack modules.

### 3. Webpack Loader Module Analysis
- Add a breakpoint before the `ep` or `eh` function, and force refresh the page with `Ctrl+Shift+R` (the loader loads when the page is first refreshed). After the breakpoint is triggered, enter the `eo` loader.
- Observe that the loader is a self-executing function `!function(parameters){loader execution logic}(functional module)`, but the functional module and parameters are missing; through context analysis, it is found that the functional module is mounted on the loader `p` (`p.m = s`).
- Execute `eo.m` in the browser console to obtain the functional module in dictionary form, then locate the target encryption function via `eo.m[18543]`, and fully extract the functional module logic of the loader.

### 4. Encryption Algorithm Identification
By analyzing the output result of the loader module, it is confirmed that the core encryption algorithm is the **unsalted MD5 digest algorithm**.

## Follow-up Operations
Organize the reversely obtained JS code, extract the Webpack loader module and supplement the running environment, then the `signature` value and the final `x-zse-96` parameter value can be generated.
