#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<math.h>
#include<string.h>
#include<math.h>
char mem[0xffff][17];
char R[8][17];

int negcheck(char* for_check, int start_digit, int end_digit)
{
	int i;
	char new[17];
	int for_return = 0;
    int time;

	//printf("negcheck in use\n");
	for (i = 0; i < 16; i++)
		new[i] = 0;
	for (i = start_digit; i <= end_digit; i++)
		new[i] = for_check[i];

	if (new[start_digit] == 1)
	{
		//printf("it is a neg number\n");
		new[start_digit] = 0;
		for (i = start_digit + 1; i <= end_digit; i++)
			new[i] = 1 - new[i];
		//new[end_digit]++;
		for (i = end_digit; i > start_digit; i--)
		{
			if (new[i] == 2)
			{
			    new[i] = 0;
				new[i - 1]++;
			}
			if (new[i] == 3)
			{
				new[i] = 1;
				new[i - 1]++;
			}
		}
		time = end_digit - start_digit;
		for (i = start_digit; i <= end_digit; i++)
		{
			for_return = for_return + new[i] * pow(2, time);
			time--;
		}
		return -for_return;
	}
	else
	{
		time = end_digit - start_digit;
		for (i = start_digit; i <= end_digit; i++)
		{
			for_return = for_return + new[i] * pow(2, time);
		    time--;
		}
		return for_return;
	}
}

int toDecimal(char* str, int start_digit, int end_digit)
{
	int for_return = 0;
	int i;
	int time;
	time = end_digit - start_digit;
	for (i = start_digit; i <= end_digit; i++)
	{
		for_return = for_return + str[i] * pow(2, time);
		time--;
	}
	return for_return;
}

void toBinary(int for_change, char* str)
{
	int i = 15;

	if (for_change < 0)
	{
		while (for_change < 0)
		{
			str[i] = for_change % 2;
			//printf(" %d", str[i]);		//我倒要看看你转出来了个什么
			i--;
			for_change = for_change / 2;
		}
		for (;i>=0; i--)
			str[i] = 1;
		//printf(" is the binary \n");
	}
	else
	{
		while (for_change > 0)
		{
			str[i] = for_change % 2;
			//printf(" %d", str[i]);		//我倒要看看你转出来了个什么
			i--;
			for_change = for_change / 2;
		}
		for (; i >= 0; i--)
			str[i] = 0;
		//printf(" is the binary \n");
	}



//这个地方不对：for_change的值已经改变，正负号也跟之前不一样
}

void check(char* str)
{
	int i;
	//printf("check in use \n");
	for (i = 15; i >= 0; i--)
	{
		//printf("%d ", str[i]);
		if (str[i] == 2)
		{
			str[i] = 0;
			str[i - 1] = str[i - 1] + 1;
			//printf("found 2\n");
		}
		if (str[i] == 3)
		{
			str[i] = 1;
			str[i - 1] = str[i - 1] + 1;
			//printf("found 3\n");
		}

	}
	//printf("\n");
}
int nzp(int for_judge)
{
	if (for_judge == 0)
		return 0;
	if (for_judge > 0)
		return 1;
	if (for_judge < 0)
		return -1;
}
int main()
{
	int PSR = 0;					//nzp
	int PC;
	char for_copy[16] = { 0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1 };		//0x7777
	int i, j;

	//initialize to x7777
	for (i = 0; i < 0xffff; i++)
		memcpy(mem[i], for_copy, 16);
	for (i = 0; i < 8; i++)
		memcpy(R[i], for_copy, 16);

	//input
	char first_line[16];
	scanf("%s", first_line);
	for (i = 15; i >= 0; i--)
	{
		first_line[i] -= '0';
	}
	int FL;
	FL = toDecimal(first_line, 0, 15);
	PC = FL;
	int JSR_in_use = 0;

	for (i = 0; i < 16; i++)
		mem[FL-1][i] = first_line[i];

	//printf("0x%x\n", PC);
	while (scanf("%s", mem[PC]) != EOF)
	{
		for (j = 0; j < 16; j++)
		{
			mem[PC][j] -= '0';
		}
		PC++;
	}
	int inst_end;
	inst_end = PC;

	int DR = 0;
	int SR1 = 0, SR2 = 0;
	int BaseR = 0;
	int PCoffset = 0;

	//loop the instructions
	//printf("%x %x %x\n", FL, inst_end, PC);
	for (PC = FL; PC <= inst_end; PC++)
	{
		//printf("first 4 digits = %d%d%d%d\n", mem[PC][0], mem[PC][1], mem[PC][2], mem[PC][3]);
		//BR:read nzp and judge, if possible, PC+-
		if (mem[PC][0] == 0 && mem[PC][1] == 0 && mem[PC][2] == 0 && mem[PC][3] == 0)
		{
			PCoffset = negcheck(mem[PC], 7, 15);
			if ((mem[PC][4] == 0 && PSR < 0) || (mem[PC][5] == 0 && PSR == 0) || (mem[PC][6] == 0 && PSR > 0))
				printf("not fitting\n");
			else
			{
				PC = PC + PCoffset;
			}
			//printf("BR: PC=%x, PSR=%d%d%d, CC=%d, PCoffset=%x \n", PC, mem[PC][4], mem[PC][5], mem[PC][6], PSR, PCoffset);
		}
		//JSR, PC+-
		else if (mem[PC][0] == 0 && mem[PC][1] == 1 && mem[PC][2] == 0 && mem[PC][3] == 0)
		{
			if (mem[PC][4] == 1)
			{
				PCoffset = negcheck(mem[PC], 5, 15);
				toBinary(PC, R[7]);
				PC = PC + PCoffset;
			}
			else if (mem[PC][4] == 0)
			{
				BaseR = toDecimal(mem[PC], 7, 9);
				toBinary(PC, R[7]);
				PC = toDecimal(R[BaseR], 0, 15)-1;
			}
			JSR_in_use++;
			//printf("JSR: PC=%x, CC=%d, BaseR=%d, PCoffset=%x \n", PC, PSR, BaseR, PCoffset);
		}
		//JMP:PC+-
		else if (mem[PC][0] == 1 && mem[PC][1] == 1 && mem[PC][2] == 0 && mem[PC][3] == 0)
		{
			BaseR = toDecimal(mem[PC], 7, 9);
			PC = toDecimal(R[BaseR], 0, 15);

			//当寄存器是R7时，=RET
			//printf("JSR: PC=%x, CC=%d, BaseR=%d , PCoffset=%x \n", PC, PSR, BaseR, PCoffset);
		}
		//ADD:register+-, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 0 && mem[PC][2] == 0 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			SR1 = toDecimal(mem[PC], 7, 9);
			if (mem[PC][10] == 1)
			{
				//R[DR] = R[SR1] + imm;
				for (i = 15; i >= 11; i--)
					R[DR][i] = R[SR1][i] + mem[PC][i];
				if (mem[PC][11] == 0)
					for (i = 10; i >= 0; i--)
						R[DR][i] = R[SR1][i];
				else
					for (i = 10; i >= 0; i--)
						R[DR][i] = R[SR1][i] + 1;
			}
			else if (mem[PC][10] == 0)
			{
				SR2 = toDecimal(mem[PC], 13, 15);
				for (i = 15; i >= 0; i--)
					R[DR][i] = R[SR1][i] + R[SR2][i];
			}
			check(R[DR]);
			PSR = nzp(toDecimal(R[DR], 0, 15));
			//printf("ADD: PC=%x, CC=%d, DR=%d, SR1=%d, SR2=%d \n", PC, PSR, DR, SR1, SR2);
		}
		//AND:&register, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 1 && mem[PC][2] == 0 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			SR1 = toDecimal(mem[PC], 7, 9);
			if (mem[PC][10] == 1)		//imm
			{
				for (i = 15; i >= 11; i--)
					R[DR][i] = R[SR1][i] & mem[PC][i];
				if (mem[PC][11] == 0)
					for (i = 10; i >= 0; i--)
						R[DR][i] = R[SR1][i] & 0;
				if (mem[PC][11] == 1)
					for (i = 10; i >= 0; i--)
						R[DR][i] = R[SR1][i] & 1;
			}
			else if (mem[PC][10] == 0)		//sr
			{
				SR2 = toDecimal(mem[PC], 13, 15);
				for (i = 15; i >= 0; i--)
					R[DR][i] = R[SR1][i] & R[SR2][i];
			}
			check(R[DR]);
			PSR = nzp(toDecimal(R[DR], 0, 15));
			//printf("AND: PC=%x, CC=%d, DR=%d, SR1=%d, SR2=%d, imm=%d \n", PC, PSR, DR, SR1, SR2, toDecimal(mem[PC], 11, 15));
		}
		//NOT:^register, PSR change
		else if (mem[PC][0] == 1 && mem[PC][1] == 0 && mem[PC][2] == 0 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			SR1 = toDecimal(mem[PC], 7, 9);
			for (i = 15; i >= 0; i--)
				R[DR][i] = 1 - R[SR1][i];
			check(R[DR]);
			PSR = nzp(toDecimal(R[DR], 0, 15));
			//printf("NOT: PC=%x, CC=%d, DR=%d, SR1=%d \n", PC, PSR, DR, SR1);
		}
		//LD: memory->register, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 0 && mem[PC][2] == 1 && mem[PC][3] == 0)
		{
			DR = toDecimal(mem[PC], 4, 6);
			PCoffset = negcheck(mem[PC], 7, 15);
			for (i = 0; i < 16; i++)
				R[DR][i] = mem[PC + PCoffset + 1][i];
			PSR = nzp(toDecimal(R[DR], 0, 15));

			//printf("LD: PC=%x, CC=%d, DR=%d, PCoffset=%d \n", PC, PSR, DR, PCoffset);

		}
		//LDR: memory->register, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 1 && mem[PC][2] == 1 && mem[PC][3] == 0)
		{
			DR = toDecimal(mem[PC], 4, 6);
			BaseR = toDecimal(mem[PC], 7, 9);
			PCoffset = negcheck(mem[PC], 10, 15);
			for (i = 0; i < 16; i++)
				R[DR][i] = mem[toDecimal(R[BaseR], 0, 15) + PCoffset][i];
			PSR = nzp(toDecimal(R[DR], 0, 15));

			//printf("LDR: PC=%x, CC=%d, DR=%d, BaseR=%d, PCoffset=%d \n", PC, PSR, DR, BaseR, PCoffset);

		}
		//LDI: memory->register, PSR change
		else if (mem[PC][0] == 1 && mem[PC][1] == 0 && mem[PC][2] == 1 && mem[PC][3] == 0)
		{
			DR = toDecimal(mem[PC], 4, 6);
			PCoffset = negcheck(mem[PC], 7, 15);
			for (i = 0; i < 16; i++)
				R[DR][i] = mem[toDecimal(mem[PC + PCoffset + 1], 0, 15)][i];

			PSR = nzp(toDecimal(R[DR], 0, 15));
			//printf("LDI: PC=%x, CC=%d, DR=%d, mem[mem[PC+PCoffset]]=%x, PCoffset=%d \n", PC, PSR, toDecimal(R[DR], 0, 15), toDecimal(mem[toDecimal(mem[PC + PCoffset], 0, 15)], 0, 15), PCoffset);

		}
		//LEA: memory location->register
		else if (mem[PC][0] == 1 && mem[PC][1] == 1 && mem[PC][2] == 1 && mem[PC][3] == 0)
		{
			DR = toDecimal(mem[PC], 4, 6);
			PCoffset = negcheck(mem[PC], 7, 15);
			//printf("%x\n", PC + PCoffset+1);
			toBinary(PC + PCoffset+1, R[DR]);
			//for (i = 0; i < 16; i++)
				//printf("%d", R[DR][i]);
			//printf("\n");
			//printf("LEA: PC=%x, CC=%d, DR=%d, PCoffset=%d \n", PC, PSR, DR, PCoffset);
		}
		//ST: register->memory, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 0 && mem[PC][2] == 1 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			PCoffset = negcheck(mem[PC], 7, 15);
			for (i = 0; i < 16; i++)
				mem[PC + PCoffset + 1][i] = R[DR][i];
			PSR = nzp(toDecimal(R[DR], 0, 15));

			//printf("ST: PC=%x, CC=%d, DR=%d, PCoffset=%d \n", PC, PSR, DR, PCoffset);

		}
		//STR: register->memory, PSR change
		else if (mem[PC][0] == 0 && mem[PC][1] == 1 && mem[PC][2] == 1 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			BaseR = toDecimal(mem[PC], 7, 9);
			PCoffset = negcheck(mem[PC], 10, 15);
			for (i = 0; i < 16; i++)
				mem[toDecimal(R[BaseR], 0, 15) + PCoffset][i] = R[DR][i];
			PSR = nzp(toDecimal(R[DR], 0, 15));

			//printf("STR: PC=%x, CC=%d, DR=%d, BaseR=%d, PCoffset=%d \n", PC, PSR, DR, BaseR, PCoffset);


		}
		//STI: register->memory, PSR change
		else if (mem[PC][0] == 1 && mem[PC][1] == 0 && mem[PC][2] == 1 && mem[PC][3] == 1)
		{
			DR = toDecimal(mem[PC], 4, 6);
			PCoffset = negcheck(mem[PC], 7, 15);
			for (i = 0; i < 16; i++)
				mem[toDecimal(mem[PC + PCoffset + 1], 0, 15)][i] = R[DR][i];
			PSR = nzp(toDecimal(R[DR], 0, 15));

			//printf("STI: PC=%x, CC=%d, DR=%d, PCoffset=%d \n", PC, PSR, DR, PCoffset);

		}
		//TRAP
		else if (mem[PC][0] == 1 && mem[PC][1] == 1 && mem[PC][2] == 1 && mem[PC][3] == 1)
		{
			//printf("TRAP\n");
			break;
		}
		//test
		//for (i = 0; i < 8; i++)
		//{
			//printf("R%d = ", i);
			//for (j = 0; j < 16; j++)
				//printf("%d ", R[i][j]);
			//printf("%x", toDecimal(R[i], 0, 15));
			//printf("\n");
		//}
	}

	//out
	for (i = 0; i < 7; i++)
		printf("R%d = x%04X\n", i, toDecimal(R[i], 0, 15));
		printf("R7 = x%04X\n", toDecimal(R[7], 0, 15)+JSR_in_use);
	return 0;
}