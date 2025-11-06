## Windows BLE Tool for Programming IR Buttons on TLSR827x Remotes  
### (Google G10, Homatics B21, etc.)
Based on [Genius1237/g10-ir](https://github.com/Genius1237/g10-ir)
 
1. **Install Python (with PATH):**
   https://www.python.org/
3. **Upgrade pip:**   
```python -m pip install --upgrade pip```  
4. **Install Bleak library:**  
```python pip install bleak```  
or  
```python -m pip install bleak```

5. Run the script, replacing the MAC with your device address:  
```python ir_win.py AA-BB-CC-EE-FF-11```  
6. Put your remote in pairing mode (press BACK + HOME on the remote)

**References**
> https://fcc.report/FCC-ID/OZ5C009/5122343.pdf  
> https://manuals.plus/ohsung-electronics/c009-rf-remote-control-unit-manual  
> https://android.googlesource.com/platform/hardware/telink/atv/refDesignRcu
