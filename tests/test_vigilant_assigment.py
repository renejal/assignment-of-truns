from typing import List
import pytest
from dominio.model.day import Day
from dominio.model.shift import Shift
from dominio.model.site import Site
from dominio.model.week import Week
from dominio.model.working_day import workingDay
from dominio.vigilant_assigment import VigilantAssigment
from services.shifts_generation_service import Shifts_generation_service

@pytest.mark.parametrize("site, ideal_hours_amount_to_work, expected", [
    #Aleatory day case
    (      
        Site("",1,False,[
            Week("", [
                Day("",2, [
                    workingDay("",6,23,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(54,62,0),
            Shift(63,71,0),
        ]
    ),
    #Full day working 24 hours case with start at 0 a.m
    (      
        Site("",1,False,[
            Week("", [
                Day("",0, [
                    workingDay("",0,23,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(0,7,0),
            Shift(8,15,0),
            Shift(16,23,0)
        ]
    ),
    #Full day working 24 hours case with start at 6 a.m
    (      
        Site("",1,False,[
            Week("", [
                Day("",0, [
                    workingDay("",6,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,5,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(6,13,0),
            Shift(14,21,0),
            Shift(22,29,0)
        ]
    ),
    #Full 2 week working ending at 6 from other day
    (      
        Site("",1,False,[
            Week("", [
                Day("",0, [
                    workingDay("",6,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",2, [
                    workingDay("",0,23,0)
                ]),
                Day("",3, [
                    workingDay("",0,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ]),
            Week("", [
                Day("",0, [
                    workingDay("",0,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",2, [
                    workingDay("",0,23,0)
                ]),
                Day("",3, [
                    workingDay("",0,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ]),
            Week("", [
                Day("",0, [
                    workingDay("",0,6,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(6,13,0),
            Shift(14,21,0),
            Shift(22,29,0),
            Shift(30,37,0),
            Shift(38,45,0),
            Shift(46,53,0),
            Shift(54,61,0),
            Shift(62,69,0),
            Shift(70,77,0),
            Shift(78,85,0),
            Shift(86,93,0),
            Shift(94,101,0),
            Shift(102,109,0),
            Shift(110,117,0),
            Shift(118,125,0),
            Shift(126,133,0),
            Shift(134,141,0),
            Shift(142,149,0),
            Shift(150,157,0),
            Shift(158,165,0),
            Shift(166,173,0),
            Shift(174,181,0),
            Shift(182,189,0),
            Shift(190,197,0),
            Shift(198,205,0),
            Shift(206,213,0),
            Shift(214,221,0),
            Shift(222,229,0),
            Shift(230,237,0),
            Shift(238,245,0),
            Shift(246,253,0),
            Shift(254,261,0),
            Shift(262,269,0),
            Shift(270,277,0),
            Shift(278,285,0),
            Shift(286,293,0),
            Shift(294,301,0),
            Shift(302,309,0),
            Shift(310,317,0),
            Shift(318,325,0),
            Shift(326,333,0),
            Shift(334,341,0),
        ]
    ),
    #Full 2 week working ending at end sunday
    (      
        Site("",1,False,[
            Week("", [
                Day("",0, [
                    workingDay("",6,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",2, [
                    workingDay("",0,23,0)
                ]),
                Day("",3, [
                    workingDay("",0,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ]),
            Week("", [
                Day("",0, [
                    workingDay("",0,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",2, [
                    workingDay("",0,23,0)
                ]),
                Day("",3, [
                    workingDay("",0,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(6,13,0),
            Shift(14,21,0),
            Shift(22,29,0),
            Shift(30,37,0),
            Shift(38,45,0),
            Shift(46,53,0),
            Shift(54,61,0),
            Shift(62,69,0),
            Shift(70,77,0),
            Shift(78,85,0),
            Shift(86,93,0),
            Shift(94,101,0),
            Shift(102,109,0),
            Shift(110,117,0),
            Shift(118,125,0),
            Shift(126,133,0),
            Shift(134,141,0),
            Shift(142,149,0),
            Shift(150,157,0),
            Shift(158,165,0),
            Shift(166,173,0),
            Shift(174,181,0),
            Shift(182,189,0),
            Shift(190,197,0),
            Shift(198,205,0),
            Shift(206,213,0),
            Shift(214,221,0),
            Shift(222,229,0),
            Shift(230,237,0),
            Shift(238,245,0),
            Shift(246,253,0),
            Shift(254,261,0),
            Shift(262,269,0),
            Shift(270,277,0),
            Shift(278,285,0),
            Shift(286,293,0),
            Shift(294,301,0),
            Shift(302,309,0),
            Shift(310,317,0),
            Shift(318,326,0),
            Shift(327,335,0),
        ]
    ),
    #create alatory strange schedule case
    (      
        Site("",1,False,[
            Week("", [
                Day("",0, [
                    workingDay("",6,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",2, [
                    workingDay("",0,5,0)
                ]),
                Day("",3, [
                    workingDay("",6,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ]),
            Week("", [
                Day("",0, [
                    workingDay("",0,23,0)
                ]),
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",3, [
                    workingDay("",0,23,0)
                ]),
                Day("",4, [
                    workingDay("",0,23,0)
                ]),
                Day("",5, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(6,13,0),
            Shift(14,21,0),
            Shift(22,29,0),
            Shift(30,37,0),
            Shift(38,45,0),
            Shift(46,53,0),
            Shift(78,85,0),
            Shift(86,93,0),
            Shift(94,101,0),
            Shift(102,109,0),
            Shift(110,117,0),
            Shift(118,125,0),
            Shift(126,133,0),
            Shift(134,141,0),
            Shift(142,149,0),
            Shift(150,157,0),
            Shift(158,165,0),
            Shift(166,173,0),
            Shift(174,181,0),
            Shift(182,189,0),
            Shift(190,197,0),
            Shift(198,206,0),
            Shift(207,215,0),
            Shift(240,247,0),
            Shift(248,255,0),
            Shift(256,263,0),
            Shift(264,271,0),
            Shift(272,279,0),
            Shift(280,287,0),
            Shift(288,295,0),
            Shift(296,303,0),
            Shift(304,311,0),
            Shift(312,319,0),
            Shift(320,327,0),
            Shift(328,335,0),
        ]
    ),
    (
        Site("",1,False,[
            Week("", [
                Day("",1, [
                    workingDay("",0,23,0)
                ]),
                Day("",6, [
                    workingDay("",0,23,0)
                ])
            ]),
            Week("", [
                Day("",1, [
                    workingDay("",0,23,0)
                ])
            ])
        ]),
        { 
            0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6],7:[7],8:[8],9:[9],10:[10],
            11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],
            19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],23:[8,8,7],24:[8,8,8]
        },
        [
            Shift(24,31,0),
            Shift(32,39,0),
            Shift(40,47,0),
            Shift(144,151,0),
            Shift(152,159,0),
            Shift(160,167,0),
            Shift(192,199,0),
            Shift(200,207,0),
            Shift(208,215,0)
        ]
    )
])
def test_create_normal_shifts_correctly(site: Site, ideal_hours_amount_to_work: int, expected: List[Shift]):
    VigilantAssigment.total_weeks= len(site.weeks_schedule)
    shifts = Shifts_generation_service.create_shifts_in_normal_sites(VigilantAssigment,site,ideal_hours_amount_to_work)
    assert len(expected) == len(shifts)
    for shiftIndex in range(len(shifts)):
        assert expected[shiftIndex].shift_start == shifts[shiftIndex].shift_start
        assert expected[shiftIndex].shift_end== shifts[shiftIndex].shift_end
@pytest.mark.parametrize("site, expected", [
    #Aleatory day case
    (
        Site("",1,True,[
            Week("", [
                Day("",1, [
                    workingDay("",6,14,0),
                    workingDay("",15,23,0)
                ])
            ])
        ]),
        [
            Shift(30,38,0),
            Shift(39,47,0)
        ]        
    ),
    #Full day working 24 hours case with start at 0 a.m
    (
        Site("",1,True,[
                Week("", [
                    Day("",1, [
                        workingDay("",0,11,0),
                        workingDay("",12,23,0)
                    ])
                ])
            ]),
        [
            Shift(24,35,0),
            Shift(36,47,0)
        ]        
    ),
    #Full day working 24 hours case with start at 6 a.m
    (
        Site("",1,True,[
                Week("", [
                    Day("",0, [
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",1, [
                        workingDay("",0,5,0)
                    ])
                ])
            ]),
        [
            Shift(6,17,0),
            Shift(18,29,0)
        ]
    ),
    #Full 2 week working ending at 6 from other day
    (
        Site("",1,True,[
                Week("", [
                    Day("",0, [
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",1, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",2, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",3, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",4, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",5, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",6, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ])
                ]),
                Week("", [
                    Day("",0, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",1, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",2, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",3, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",4, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",5, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",6, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ])
                ]),
                Week("",[
                    Day("",0,[
                        workingDay("",0,5,0)
                    ])
                ])
            ]),
        [
            Shift(6,17,0),
            Shift(18,29,0),
            Shift(30,41,0),
            Shift(42,53,0),
            Shift(54,65,0),
            Shift(66,77,0),
            Shift(78,89,0),
            Shift(90,101,0),
            Shift(102,113,0),
            Shift(114,125,0),
            Shift(126,137,0),
            Shift(138,149,0),
            Shift(150,161,0),
            Shift(162,173,0),
            Shift(174,185,0),
            Shift(186,197,0),
            Shift(198,209,0),
            Shift(210,221,0),
            Shift(222,233,0),
            Shift(234,245,0),
            Shift(246,257,0),
            Shift(258,269,0),
            Shift(270,281,0),
            Shift(282,293,0),
            Shift(294,305,0),
            Shift(306,317,0),
            Shift(318,329,0),
            Shift(330,341,0)
        ]
    ),
    #Full 2 week working ending at end sunday
    (
        Site("",1,True,[
                Week("", [
                    Day("",0, [
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",1, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",2, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",3, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",4, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",5, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",6, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ])
                ]),
                Week("", [
                    Day("",0, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",1, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",2, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",3, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",4, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",5, [
                        workingDay("",0,5,0),
                        workingDay("",6,17,0),
                        workingDay("",18,23,0)
                    ]),
                    Day("",6, [
                        workingDay("",0,5,0),
                        workingDay("",6,14,0),
                        workingDay("",15,23,0)
                    ])
                ])
            ]),
        [
            Shift(6,17,0),
            Shift(18,29,0),
            Shift(30,41,0),
            Shift(42,53,0),
            Shift(54,65,0),
            Shift(66,77,0),
            Shift(78,89,0),
            Shift(90,101,0),
            Shift(102,113,0),
            Shift(114,125,0),
            Shift(126,137,0),
            Shift(138,149,0),
            Shift(150,161,0),
            Shift(162,173,0),
            Shift(174,185,0),
            Shift(186,197,0),
            Shift(198,209,0),
            Shift(210,221,0),
            Shift(222,233,0),
            Shift(234,245,0),
            Shift(246,257,0),
            Shift(258,269,0),
            Shift(270,281,0),
            Shift(282,293,0),
            Shift(294,305,0),
            Shift(306,317,0),
            Shift(318,326,0),
            Shift(327,335,0)
        ]
    )  
])
def test_create_special_shifts_correctly(site: Site,expected: List[Shift]):
    VigilantAssigment.total_weeks= len(site.weeks_schedule)
    shifts = Shifts_generation_service.create_shifts_in_normal_sites(VigilantAssigment,site)
    assert len(expected) == len(shifts)
    for shiftIndex in range(len(shifts)):
        assert expected[shiftIndex].shift_start == shifts[shiftIndex].shift_start
        assert expected[shiftIndex].shift_end== shifts[shiftIndex].shift_end
    return


