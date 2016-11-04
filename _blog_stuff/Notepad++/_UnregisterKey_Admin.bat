::创建reg文件
del %path%\_temp.reg
@echo Windows Registry Editor Version 5.00>>_temp.reg
@echo [-HKEY_CLASSES_ROOT\*\Shell\Notepad++ Here]>>_temp.reg
@echo [-HKEY_CLASSES_ROOT\*\Shell\Notepad++ Here\Command]>>_temp.reg

:: 注册.reg文件到注册表中, 然后删除
reg import _temp.reg 
del %path%\_temp.reg
