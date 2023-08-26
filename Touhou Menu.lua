local KH1Menu = 0x5af683 - 0x56454E
function _OnFrame()
	if ReadString(KH1Menu, 3) == "zz0" then 
		WriteString(KH1Menu, "zz0") --KH1 Command Menu change
	end
end

function _OnInit() end

--"al0" | "Agrabah",
--"bb0" | "Beast's Castle",
--"ca0" | "Port Royal",
--"dc0" | "Disney Castle",
--"dc1" | "Lingering Will",
--"eh0" | "The World That Never Was",
--"hb0" | "Hollow Bastion",
--"hb1" | "Garden of Assemblage",
--"hb2" | "Absent Silhouette",
--"he0" | "Olympus Coliseum",
--"he1" | "The Underworld",
--"lk0" | "Pride Lands",
--"mu0" | "Land of Dragons",
--"nm0" | "Halloween Town",
--"nm1" | "Christmas Town",
--"po0" | "100 Acre Wood",
--"tr0" | "Space Paranoids",
--"tt0" | "Twilight Town",
--"tt1" | "Station of Calling", #looks like kh1 but with classic icons.
--"tt2" | "Mysterious Tower",
--"tt3" | "Mansion Basement",
--"tt4" | "The White Room",
--"tt5" | "Mansion",
--"tt6" | "Betwixt & Between",
--"wi0" | "Timeless River",
--"zz0" | "Kingdom Hearts 1"
local Settings = 0x446D06
function _OnFrame()
	WriteShort(Settings, ReadShort(Settings) | 0x40) --Auto Cam, KH1 CCommands
end

function _OnInit() end